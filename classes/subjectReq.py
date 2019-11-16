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

from . import course
from . import degree
from . import term
from . import program
from . import singleReq

default_mark = 50

class SubjectReq(singleReq.SingleReq):

    def __init__(self, course: 'course.Course', min_mark: int=None):
        super().__init__()
        self.course = course
        if min_mark is None:
            self.min_mark = default_mark
        else:
            self.min_mark = min_mark

    def __repr__(self) -> str:
        return f"<SubjectReq course={self.course!r} min_mark={self.min_mark!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        if self.min_mark == default_mark:
            return self.course.course_code
        else:
            return "A mark of {self.min_mark} in {self.course.course_code}"

     # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return "CompletedCourseRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False) -> List[str]:
        for enrollment in program.courses:
            if enrollment.course == self.course or enrollment.course.equivalent(self.course):
                if (coreq and enrollment.term <= term) or (enrollment.term < term):
                    return []
        return[self.course.course_code]

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass

