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
        subject = self.code[0..3]
        code  = self.code[4..7]
        name = ""
        units = self.units
        terms = self.parse_terms()
        faculty = self.faculty
        prereqs = self.parse_prereqs()
        coreqs = self.parse_coreqs()
        exclusions = self.parse_exclusions()
        equivalents = self.parse_equivalents()

        return course.Course(subject, code, name, units, terms, faculty,
                    prereqs, coreqs, exclusions, equivalents)


    # Parse the string to return the list of term offerings
    def parse_terms(self) -> List['term.Term']:
        terms: List['term.Term'] = []
        for i in range(1, 4):
            if str(i) in self.terms:
                terms.append(term.Term(self.year, i))
        return terms
        # TODO summer terms

    def parse_equivalents(self):
        for c in self.equivalents:
            code = get_course_code(c)
            
