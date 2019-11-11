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

    # Input: The year of your degree you should be in to take this course
    # This could be 1, 2, 3 etc or -1 for final year, -2 for second-last etc.
    def __init__(self, year: int):
        super().__init__()
        self.year = year

    def __repr__(self) -> str:
<<<<<<< HEAD
        return "<YearReq year={self.year!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        return f"Year {self.year} in your degree"
=======
        return f"<YearReq year={self.year!r}>"
>>>>>>> master

    @property
    def requirement_name(self) -> str:
        return "YearRequirement"

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False) -> bool:
        if self.year < 0:
            if term.year == program.final_year + self.year + 1:
                return True
            return False
        elif term.year == program.intake_year + self.year - 1:
            return True
        return False


    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
