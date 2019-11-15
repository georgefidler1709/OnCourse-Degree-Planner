"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scrapedSubjectReq.py
The course requirement to have taken a specific course prior to completing this one
Skeleton class to be filled out later

[MORE INFO ABOUT CLASS]
"""

from typing import List, Optional

from classes import course
from classes import degree
from classes import term
from classes import program
from classes import singleReq
from classes import subjectReq
from classes import university


class ScrapedSubjectReq(singleReq.SingleReq):

    def __init__(self, course: str, min_mark: int=None):
        super().__init__()
        self.course = course
        if min_mark is None:
            self.min_mark = 50
        else:
            self.min_mark = min_mark

    # create function to turn into proper subjectReq
    def inflate(self, university: 'university.University') -> Optional['subjectReq.SubjectReq']:
        c = university.find_course(self.course)
        if c is not None:
            return subjectReq.SubjectReq(c, self.min_mark)
        return None

    def __repr__(self) -> str:
        return f"<SubjectReq course={self.course!r} min_mark={self.min_mark!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        pass


     # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return "CompletedCourseRequirement"

    def check(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False, excl: bool=False) -> List[str]:
        pass


    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, prog: 'program.Program', term: 'term.Term',
            coreq: bool=False, excl: bool=False) -> bool:
        pass


    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass

