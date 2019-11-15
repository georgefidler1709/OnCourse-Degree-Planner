"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scrapedCourse.py
A class to contain information about a course, scraped from the handbook

[MORE INFO ABOUT CLASS]
"""


from typing import List, Optional

from . import courseParser
from classes import course
from classes import university

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
        self.units = units

        parser = courseParser.CourseParser()

        # Type for requirements??
        self.prereqs, self.coreqs = parser.parse_reqs(self.requirements)
        self.terms = parser.parse_terms(terms, self.year)


    # Given a university with database populated excluding requirements,
    def inflate(self, university: 'university.University') -> Optional['course.Course']:
        course = university.find_course(self.code)
        if course is None:
            # ERROR
            return None
        if self.prereqs:
            course.prereqs = self.prereqs.inflate(university)
        if self.coreqs:
            course.coreqs = self.coreqs.inflate(university)

        exclusions = []
        for ex in self.exclusions:
            c = university.find_course(ex)
            if c:
                exclusions.append(c)
        course.exclusions = exclusions

        equivalents = []
        for eq in self.equivalents:
            c = university.find_course(eq)
            if c:
                equivalents.append(c)
        course.equivalents = equivalents
        return course



    # Convert to a course object
    def to_course(self) -> 'course.Course':
         # Step 1: save into db
        subject = self.code[:4]
        code  = int(self.code[4:])
        name = ""
        units = self.units
        terms = self.terms
        faculty = self.faculty

        # store in dict
        #STORE IN DB
        return course.Course(subject, code, name, units, terms, faculty)



