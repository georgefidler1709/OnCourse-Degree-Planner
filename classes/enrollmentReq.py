"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

enrollmentReq.py
The course requirement to be enrolled in a specific degree program

[MORE INFO ABOUT CLASS]
"""

from typing import List

from . import course
from . import degree
from . import term
from . import program
from . import singleReq

class EnrollmentReq(singleReq.SingleReq):

    def __init__(self, degree: degree.Degree):
        super().__init__()
        self.degree = degree

    def __repr__(self) -> str:
        return f"<EnrollmentReq degree={self.degree!r}>"

    def info(self, top_leve: bool=False, exclusion: bool=False) -> str:
        return f"Enrollment in {self.degree.name} ({self.degree.num_code})"

    @property
    def requirement_name(self) -> str:
        return "CurrentDegreeRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False, excl: bool=False) -> List[str]:
        errors = []
        if excl and program.degree == self.degree:
            errors.append(self.info())
        elif not excl and program.degree != self.degree:
            errors.append(self.info())
        return errors

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
