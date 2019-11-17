"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

dbGenerator.py
A class to generate the database based on scraping information from the handbook
"""

from mypy_extensions import DefaultArg
import requests
from sqlite3 import Row
from typing import Callable, Tuple, Optional, List

from classes import university
from classes import course
from classes import courseReq

from . import scraper

def get_webpage(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    return response.text

class dbGenerator(object):
    def __init__(self, query_db: Callable[[str, DefaultArg(Tuple), DefaultArg(bool, 'one')], Row],
            store_db: Callable[[str, DefaultArg(Tuple)], int]):
        self.query_db = query_db
        self.store_db = store_db
        self.university = university.University(self.query_db)
        self.scraper = scraper.Scraper(get_webpage)


    def generate_db(self, year: int, postgrad: bool=False) -> None:
        course_codes = self.scraper.get_course_codes(year, "", postgrad)


        scraped_courses = list(map(lambda x: self.scraper.get_course(year, x, postgrad), course_codes))

        scraped_courses_to_course_id = {}

        # First insert all of them without their prerequisites
        for scraped_course in scraped_courses:
            course = scraped_course.to_course()
            course_id = self.insert_course_without_requirements(course)

            scraped_courses_to_course_id[scraped_course] = course_id

        # Now insert all of them with their prerequisites
        for scraped_course in scraped_courses:
            course_id = scraped_courses_to_course_id[scraped_course]
            full_course = scraped_course.inflate(self.university)

            if course is not None and course.finished:
                self.insert_requirements(course_id, course.prereqs, course.coreqs, course.exclusions,
                        course.equivalents)
            else:
                print(f"Course {course.course_code} could not be parsed properly")

    def insert_course_without_requirements(self, course: 'course.Course') -> int:
        result_id = self.store_db('''insert or replace into Courses(letter_code, number_code, level, name,
        faculty, units, finished) values (?, ?, ?, ?, ?, ?, 0)''', (course.subject, course.code,
            course.level, course.name, course.faculty, course.units))

        return result_id

    def insert_requirements(self, course_id: int, prereqs: Optional['courseReq.CourseReq'], coreqs:
            Optional['courseReq.CourseReq'], exclusions: List[str], equivalents: List[str]) -> None:

        if prereqs is None:
            prereq_id = None
        else:
            prereq_id = self.store_course_requirement(prereqs)

        if coreqs is None:
            coreq_id = None
        else:
            coreq_id = self.store_course_requirement(coreqs)

        self.store_db('''update Coures set prereq = ?, coreq = ?, finished = 1 where id = ?''', (prereq_id,
            coreq_id, course_id))

        for exclusion in exclusions:
            letter_code = exclusion[:4]
            number_code = exclusion[4:]

            result = self.query_db('''select id from Courses where letter_code = ? and
            number_code = ?''', (letter_code, number_code), one=True)

            if result is None:
                raise ValueError(f"No course with code {exclusion} for exclusions")

            (exclusion_id,) = result

            if exclusion_id < course_id:
                first_id, second_id = exclusion_id, course_id
            else:
                first_id, second_id = course_id, exclusion_id

            self.store_db('''insert into ExcludedCourses(first_course, second_course) values (?, ?)''', (first_id, second_id))

        for equivalent in equivalents:
            letter_code = equivalent[:4]
            number_code = equivalent[4:]

            result = self.query_db('''select id from Courses where letter_code = ? and
            number_code = ?''', (letter_code, number_code), one=True)

            if result is None:
                raise ValueError(f"No course with code {equivalent} for equivalents")

            (equivalent_id,) = result

            if equivalent_id < course_id:
                first_id, second_id = equivalent_id, course_id
            else:
                first_id, second_id = course_id, equivalent_id

            self.store_db('''insert into EquivalentCourses(first_course, second_course) values (?, ?)''', (first_id, second_id))

    def store_course_requirement(self, requirement: 'courseReq.CourseReq') -> int:
        # Deals with everything but the standard subjectReq and enrollmentReq, as a different
        # version is used for those
        if isinstance(requirement, andReq.CompositeReq):
            # And and Or Requirements are stored the same way
            return self.store_composite_req(requirement)
        elif isinstance(requirement, uocReq.UOCReq):
            return self.store_uoc_req(requirement)
        elif isinstance(requirement, wamReq.WAMReq):
            return self.store_wam_req(requirement)
        elif isinstance(requirement, yearReq.YearReq):
            return self.store_year_req(requirement)
        elif isinstance(requirement, scrapedEnrollmentReq.ScrapedEnrollmentReq):
            return self.store_enrollment_req(requirement)
        elif isinstance(requirement, scrapedSubjectReq.ScrapedSubjectReq):
            return self.store_subject_req(requirement)
        else:
            raise NotImplementedError("Cannot store course requirement type {}".format(type(requirement)))

    def store_composite_req(self, requirement: 'compositeReq.CompositeReq') -> int:
        req_id = self.store_db('''insert into CourseRequirements(type_id) values(?)''',
                (requirement.requirement_id))

        for sub_requirement in requirement.reqs:
            sub_requirement_id = self.store_course_requirement(sub_requirement)

            self.store_db('''insert into CourseRequirementHierarchies(parent_id, child_id) values(?,
            ?)''', (req_id, sub_requirement_id))

        return req_id

    def store_uoc_req(self, requirement: 'uocReq.UOCReq'):
        if requirement.filter is not None:
            raise NotImplementedError("Cannot deal with requirements with filters currently")

        filter_id = None
        req_id = self.store_db('''insert into CourseRequirements(type_id, uoc_amount_required,
        uoc_course_filter) values(?, ?, ?)''', (requirement.requirement_id, requirement.uoc,
            filter_id))

        return req_id

    def store_wam_req(self, requirement: 'wamReq.WAMReq'):
        req_id = self.store_db('''insert into CourseRequirements(type_id, wam) values(?, ?)''',
                (requirement.requirement_id, requirement.wam))

        return req_id

    def store_year_req(self, requirement: 'yearReq.YearReq'):
        req_id = self.store_db('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (requirement.requirement_id, requirement.year))

        return req_id

    def store_enrollment_req(self, requirement: 'scrapedEnrollmentReq.ScrapedEnrollmentReq'):
        pass

    def store_subject_req(self, requirement: 'scrapedSubjectReq.ScrapedSubjectReq'):
        pass






