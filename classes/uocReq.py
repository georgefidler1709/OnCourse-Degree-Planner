"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

uocReq.py
The course requirement to have completed a certain number of units of credit prior
to enrolling, sometimes from a specific list of subjects

[MORE INFO ABOUT CLASS]
"""

from typing import List

import course
import courseFilter
import term
import program
import singleReq


class UOCReq(singleReq.SingleReq):

    def __init__(self, uoc: int, filter: courseFilter.CourseFilter=None):
        super().__init__()
        self.uoc = uoc
        self.filter = filter

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False) -> bool:
        pass
