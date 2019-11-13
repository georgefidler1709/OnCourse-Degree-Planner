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

    # Convert to a course object
    def to_course(self):
        parser = parser.Parser()

        subject = ""
        code  = 0
        name = ""
        units = self.units
        terms = parser.parse_terms(self.terms)
        faculty = self.faculty
        prereqs = parser.parse_req(self.prereqs)
        coreqs = parser.parse_req(self.coreqs)
        exclusions = parser.parse_req(self.exclusions)
        equivalents = parser.parse_eq(self.equivalents)

        return course.Course(subject, code, name, units, terms, faculty,
                    prereqs, coreqs, exclusions, equivalents)


