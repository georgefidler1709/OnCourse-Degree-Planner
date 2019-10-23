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

import course
import degree
import term
import program
import singleReq

class EnrollmentReq(singleReq.SingleReq):

    def __init__(self, degree: degree.Degree):
        super().__init__()
        self.degree = degree

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False) -> bool:
        return program.degree == self.degree
