"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

enrollmentReq.py
The course requirement to be enrolled in a specific degree program

[MORE INFO ABOUT CLASS]
"""

from typing import List

from course import Course
from degree import Degree
from program import Program
from singleReq import SingleReq

class EnrollmentReq(SingleReq):

    def __init__(self, degree: Degree):
        super().__init__()
        self.degree = degree

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: Program, term: int,
            additionalCourses: List[Course]=[], coreq: bool=False) -> bool:
        return program.degree == self.degree
