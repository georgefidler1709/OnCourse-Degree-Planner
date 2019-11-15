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
            Optional['courseReq.CourseReq'], exclusions: List[str], equivalents: List[str]):

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

    def store_course_requirement(self, requirement: 'courseReq.CourseReq'):
        raise NotImplementedError("Have not yet implemented store_course_requirement")

