"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

dbGenerator.py
A class to generate the database based on scraping information from the handbook
"""

import requests

from classes import university

from . import scraper

def get_webpage(url: str) -> str:
    response = requests.get(url)
    response.raise_for_status()

    return response.text

class dbGenerator(object):
    def __init__(self, query_db: Callable[[str, DefaultArg(Tuple), DefaultArg(bool, 'one')], Row],
            store_db: Callable[[str, DefaultArg(Tuple)], None]):
        self.query_db = query_db
        self.store_db = store_db
        self.university = university.University(self.query_db)
        self.scraper = scraper.Scraper(get_webpage)

    def generate_db(year: int, postgrad: bool=False) -> None:
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
            requirements = scraped_course.get_reqs()

            self.insert_requirements(course_id, requirements)


