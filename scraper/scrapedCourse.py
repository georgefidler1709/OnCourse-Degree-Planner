"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scrapedCourse.py
A class to contain information about a course, scraped from the handbook

[MORE INFO ABOUT CLASS]
"""


from typing import List

from . import courseParser
from classes import course

class ScrapedCourse(object):
    def __init__(self,
            year: int,
            code: str,
            overview: str,
            equivalents: List[str],
            exclusions: List[str],
            requirements: str,
            faculty: str,
            school: str,
            study_level: str,
            terms: str,
            units: int):
        self.year = year
        self.code = code
        self.overview = overview
        self.equivalents = equivalents
        self.exclusions = exclusions
        self.requirements = requirements
        self.faculty = faculty
        self.school = school
        self.study_level = study_level
        self.terms = terms
        self.units = units

    def save_to_dict(self) -> List['course.Course']:
        pass

    # Convert to a course object
    def to_course(self) -> 'course.Course':
        parser = courseParser.CourseParser()

        # Step 1: save into db
        subject = ""
        code  = 0
        name = ""
        units = self.units
        terms = parser.parse_terms(self.terms, self.year)
        faculty = self.faculty

        # store in dict
        return course.Course(subject, code, name, units, terms, faculty)

    def fill_reqs(self):
        parser = courseParser.CourseParser()

        prereqs = parser.parse_req(self.prereqs)
        coreqs = parser.parse_req(self.coreqs)
        exclusions = parser.parse_req(self.exclusions)
        equivalents = parser.parse_eq(self.equivalents)

        return course.Course(subject, code, name, units, terms, faculty,
                    prereqs, coreqs, exclusions, equivalents)


