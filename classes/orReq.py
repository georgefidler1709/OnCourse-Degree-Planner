"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

orReq.py
A course requirement that requires at least one of multiple requirements to be matched

[MORE INFO ABOUT CLASS]
"""

from typing import List

from compositeReq import CompositeReq
from course import Course
from courseReq import CourseReq
from program import Program

class OrReq(CompositeReq):

    def __init__(self, reqs: List[CourseReq]):
        super().__init__(reqs)

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: Program, term: int,
            additional_courses: List[Course]=[], coreq: bool=False) -> bool:
        individual_fulfills = map(lambda x: x.fulfilled(program, term, additional_courses, coreq),
                self.reqs)

        # Accept if any of the requirements are fulfilled
        return any(individual_fulfills)
