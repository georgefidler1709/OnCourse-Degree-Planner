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
        return f"<YearReq year={self.year!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        if self.year == -1:
            return f"Final year in your degree"
        return f"Year {self.year} in your degree"

    @property
    def requirement_name(self) -> str:
        return "YearRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False) -> List[str]:
        if program.matching_year(term, self.year):
            return []
        else:
            return [self.info()]

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
