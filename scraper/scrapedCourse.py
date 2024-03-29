'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scrapedCourse.py
A class to contain information about a course, scraped from the handbook
'''


from typing import List, Optional

from . import courseParser
from classes import course
from classes import university
from classes import unparsedReq

class ScrapedCourse(object):
    def __init__(self,
            year: int,
            code: str,
            name: str,
            units: int,
            overview: str,
            equivalents: List[str],
            exclusions: List[str],
            requirements: str,
            faculty: str,
            school: str,
            study_level: str,
            terms: str):
        self.year = year
        self.code = code
        self.name = name
        self.units = units
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
        # make sure these return none if can't parse
        self.prereqs, self.coreqs, self.finished = parser.parse_reqs(self.requirements)

        if not self.finished:
            print(f'Could not parse requirements for {self.code}')
            self.prereqs = unparsedReq.UnparsedReq(self.requirements)

        self.terms = parser.parse_terms(terms, self.year)

    # Parses requirements again (for use after updating requirements)
    def reparse(self) -> None:
        parser = courseParser.CourseParser()
        self.prereqs, self.coreqs, self.finished = parser.parse_reqs(self.requirements)


    # Convert to a course object
    def to_course(self) -> 'course.Course':
         # Step 1: save into db
        subject = self.code[:4]
        code  = self.code[4:]
        name = self.name
        units = self.units
        terms = self.terms
        faculty = self.faculty
        prereqs = self.prereqs
        coreqs = self.coreqs

        # store in dict
        #STORE IN DB
        return course.Course(subject, code, name, units, terms, faculty, prereqs=self.prereqs,
                coreqs=self.coreqs, exclusions=self.exclusions, equivalents=self.equivalents,
                finished=self.finished)


