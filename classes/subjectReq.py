"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

subjectReq.py
The course requirement to have taken a specific course prior to completing this one

[MORE INFO ABOUT CLASS]
"""

from typing import List

import course
import degree
import term
import program
import singleReq


class SubjectReq(singleReq.SingleReq):

    def __init__(self, course: course.Course, min_mark: int=None):
        super().__init__()
        self.course = course
        if min_mark is None:
            self.min_mark = 50
        else:
            self.min_mark = min_mark

     # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return "CompletedCourseRequirement"

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False) -> bool:
        for enrollment in program.courses:
            if enrollment.course == self.course:
                if (coreq and enrollment.term <= term) or (enrollment.term < term):
                    return True
        return False
    
    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass

