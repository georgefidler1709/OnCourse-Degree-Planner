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

import course
import term
import program
import singleReq


class YearReq(singleReq.SingleReq):

    def __init__(self, year: int):
        super().__init__()
        self.year = year

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            additional_courses: List[course.Course]=[], coreq: bool=False) -> bool:
        pass
