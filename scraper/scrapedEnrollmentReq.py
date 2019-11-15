"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scrapedEnrollmentReq.py
The course requirement to be enrolled in a specific degree program
A skeleton class for webscraper

[MORE INFO ABOUT CLASS]
"""

from typing import List, Optional

from classes import course
from classes import degree
from classes import term
from classes import program
from classes import singleReq
from classes import enrollmentReq
from classes import university

class ScrapedEnrollmentReq(singleReq.SingleReq):

    def __init__(self, degree: int):
        super().__init__()
        self.degree = degree

    def __repr__(self) -> str:
        return f"<EnrollmentReq degree={self.degree!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        pass

    @property
    def requirement_name(self) -> str:
        return "CurrentDegreeRequirement"

    def check(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False, excl: bool=False) -> List[str]:
        pass


    # turn into proper EnrollmentReq
    def inflate(self, university: 'university.University') -> Optional['enrollmentReq.EnrollmentReq']:
        d = university.find_degree_number_code(self.degree)
        if d:
            return enrollmentReq.EnrollmentReq(d)
        else:
            return None


    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False, excl: bool=False) -> bool:
        pass

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
