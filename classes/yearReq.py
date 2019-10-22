"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

yearReq.py
The course requirement to be in a specific year of a degree before enrolling

[MORE INFO ABOUT CLASS]
"""

from typing import List

from course import Course
from program import Program
from singleReq import SingleReq

class YearReq(SingleReq):

    def __init__(self, year: int):
        super().__init__()
        self.year = year

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: Program, term: int,
            additionalCourses: List[Course]=[], coreq: bool=False) -> bool:
        pass
