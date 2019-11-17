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

from classes import (
        university,
        andReq,
        compositeReq,
        course,
        courseReq,
        uocReq,
        wamReq,
        yearReq
)


from . import scraper
from . import scrapedEnrollmentReq
from . import scrapedSubjectReq

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


    # Scrapes all of the information from the handbook for the given year and the given fields, and
    # adds sessions for each of them up until the provided end year
    def generate_db(self, year: int, fields: List[str]=[""], postgrad: bool=False, end_year:
            Optional[int]=None) -> None:

        if end_year is None:
            end_year = year

        course_codes: List[str] = []
        for field in fields:
            course_codes += self.scraper.get_course_codes(year, field, postgrad)


        scraped_courses = list(map(lambda x: self.scraper.get_course(year, x, postgrad), course_codes))

        scraped_courses_to_course_id = {}

        # First insert all of them without their prerequisites
        for scraped_course in scraped_courses:
            course = scraped_course.to_course()
            course_id = self.insert_course_without_requirements(course, start_year=year, end_year=end_year)

            scraped_courses_to_course_id[scraped_course] = course_id

        # Now insert all of them with their prerequisites
        for scraped_course in scraped_courses:
            course_id = scraped_courses_to_course_id[scraped_course]
            full_course = scraped_course.to_course()

            if full_course is not None and full_course.finished:
                self.insert_requirements(course_id, full_course.prereqs, full_course.coreqs,
                        full_course.exclusions, full_course.equivalents)
            else:
                print(f"Course {course.course_code} could not be parsed properly")

    def insert_course_without_requirements(self, course: 'course.Course', start_year: int,
            end_year: Optional[int]=None) -> int:
        if end_year is None:
            end_year = start_year
        result_id = self.store_db('''insert or replace into Courses(letter_code, number_code, level, name,
        faculty, units, finished) values (?, ?, ?, ?, ?, ?, 0)''', (course.subject, course.code,
            course.level, course.name, course.faculty, course.units))

        for year in range(start_year, end_year+1):
            for term in course.terms:
                self.store_db('''insert or ignore into Sessions(year, term) values(?, ?)''',
                        (year, term.term))

                self.store_db('''insert into CourseOfferings(course_id, session_year, session_term)
                values(?, ?, ?)''', (result_id, year, term.term))

        return result_id

    def insert_requirements(self, course_id: int, prereqs: Optional['courseReq.CourseReq'], coreqs:
            Optional['courseReq.CourseReq'], exclusions: List[str], equivalents: List[str]) -> None:

        print("Exclusions are: ", exclusions)

        if prereqs is None:
            prereq_id = None
        else:
            prereq_id = self.store_course_requirement(prereqs)

        if coreqs is None:
            coreq_id = None
        else:
            coreq_id = self.store_course_requirement(coreqs)

        self.store_db('''update Courses set prereq = ?, coreq = ?, finished = 1 where id = ?''', (prereq_id,
            coreq_id, course_id))

        for exclusion in exclusions:
            exclusion_id = self.find_course(exclusion)

            if exclusion_id < course_id:
                first_id, second_id = exclusion_id, course_id
            else:
                first_id, second_id = course_id, exclusion_id

            self.store_db('''insert or ignore into ExcludedCourses(first_course, second_course) values (?, ?)''', (first_id, second_id))

        for equivalent in equivalents:
            equivalent_id = self.find_course(equivalent)

            if equivalent_id < course_id:
                first_id, second_id = equivalent_id, course_id
            else:
                first_id, second_id = course_id, equivalent_id

            self.store_db('''insert or ignore into EquivalentCourses(first_course, second_course) values (?, ?)''', (first_id, second_id))

    def store_course_requirement(self, requirement: 'courseReq.CourseReq') -> int:
        # Deals with everything but the standard subjectReq and enrollmentReq, as a different
        # version is used for those
        if isinstance(requirement, compositeReq.CompositeReq):
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
                (self.get_req_type_id(requirement.requirement_name),))

        for sub_requirement in requirement.reqs:
            sub_requirement_id = self.store_course_requirement(sub_requirement)

            self.store_db('''insert into CourseRequirementHierarchies(parent_id, child_id) values(?,
            ?)''', (req_id, sub_requirement_id))

        return req_id

    def store_uoc_req(self, requirement: 'uocReq.UOCReq'):
        if requirement.filter is not None:
            raise NotImplementedError("Cannot deal with requirements with filters currently")

        filter_id = None

        type_id = self.get_req_type_id(requirement.requirement_name)
        uoc = requirement.uoc

        result = self.query_db('''select id from CourseRequirements where type_id = ? and uoc = ?
        and filter_id = ?''', (type_id, uoc, filter_id), one=True)

        if result is not None:
            (req_id, ) = result
            return req_id

        req_id = self.store_db('''insert into CourseRequirements(type_id, uoc_amount_required,
        uoc_course_filter) values(?, ?, ?)''', (type_id, uoc, filter_id))

        return req_id

    def store_wam_req(self, requirement: 'wamReq.WAMReq'):
        type_id = self.get_req_type_id(requirement.requirement_name)
        wam = requirement.wam
        
        result = self.query_db('''select id from CourseRequirements where type_id = ? and wam =
                ?''', (type_id, wam), one=True)

        if result is not None:
            (req_id, ) = result
            return req_id

        req_id = self.store_db('''insert into CourseRequirements(type_id, wam) values(?, ?)''',
                (type_id, wam))

        return req_id

    def store_year_req(self, requirement: 'yearReq.YearReq'):
        type_id = self.get_req_type_id(requirement.requirement_name) 
        year = requirement.year

        result = self.query_db('''select id from CourseRequirements where type_id = ? and year =
        ?''', (type_id, year), one=True)

        if result is not None:
            (req_id, ) = result
            return req_id

        req_id = self.store_db('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, requirement.year))

        return req_id

    def store_enrollment_req(self, requirement: 'scrapedEnrollmentReq.ScrapedEnrollmentReq'):
        type_id = self.get_req_type_id(requirement.requirement_name)
        degree = requirement.degree

        result = self.query_db('''select id from CourseRequirements where type_id = ? and degree =
        ?''', (type_id, degree), one=True)

        if result is not None:
            (req_id, ) = result
            return req_id

        req_id = self.store_db('''insert into CourseRequirements(type_id, degree_id) values(?,
                ?)''', (type_id, degree))

        return req_id

    def store_subject_req(self, requirement: 'scrapedSubjectReq.ScrapedSubjectReq'):
        # First find the relevant course
        course_id = self.find_course(requirement.course)

        type_id = self.get_req_type_id(requirement.requirement_name)
        min_mark = requirement.min_mark

        result = self.query_db('''select id from CourseRequirements where type_id = ? and
        course_id = ? and min_mark = ?''', (type_id, course_id, min_mark), one=True)
        if result is not None:
            # One of these already exists, just return it
            (req_id, ) = result
            return req_id

        req_id = self.store_db('''insert into CourseRequirements(type_id, course_id, min_mark)
        values(?, ?, ?)''', (self.get_req_type_id(requirement.requirement_name), course_id, requirement.min_mark))

        return req_id

    def find_course(self, course_code: str):
        letter_code = course_code[:4]
        number_code = course_code[4:]

        result = self.query_db('''select id from Courses where letter_code = ? and
        number_code = ?''', (letter_code, number_code), one=True)

        course_id = None

        if result is None:
            print(f"Adding course {course_code} because it doesn't exist in the database/must be from earlier years")

            course_id = self.store_db('''insert into Courses(letter_code, number_code, level, units,
            finished, faculty, name) values(?, ?, ?, ?, ?, ?, ?)''', (letter_code, number_code,
                number_code[0], 6, 0, "Unknown Faculty", "Unknown Course Name"))
        else:
            (course_id,) = result

        return course_id

    # Gets the database id for a requirement type name
    def get_req_type_id(self, requirement_name) -> int:
        result = self.query_db('select id from CourseRequirementTypes where name = ?',
                (requirement_name, ), one=True)

        if result is None:
            raise ValueError(f"No requirement type with name {requirement_name}")

        (requirement_id,) = result
        return requirement_id




