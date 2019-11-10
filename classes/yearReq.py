"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

yearReq.py
The course requirement to be in a specific year of a degree before enrolling

[MORE INFO ABOUT CLASS]
"""

from typing import List

from . import course
from . import term
from . import program
from . import singleReq


class YearReq(singleReq.SingleReq):

    def __init__(self, year: int):
        super().__init__()
        self.year = year

    def __repr__(self) -> str:
        return "<YearReq year={self.year!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        return f"Year {self.year} in your degree"

    @property
    def requirement_name(self) -> str:
        return "YearRequirement"

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False) -> bool:
        if term.year == program.intake_year + self.year - 1:
            return True
        return False
        # TODO handle "Final Year" requirement


    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
