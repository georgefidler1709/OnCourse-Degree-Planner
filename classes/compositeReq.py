"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

compositeReq.py
A composite course requirement, where more than one requirement must be considered
Abstract class which collects the two kinds of composite requirement (AND/OR)

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from . import course
from . import courseReq
from . import term
from . import program

class CompositeReq(courseReq.CourseReq, ABC):

    def __init__(self, reqs: List[courseReq.CourseReq]):
        super().__init__()
        self.reqs = reqs # <List>courseReq.CourseReq

    @abstractmethod
    def __repr__(self) -> str:
        return f"<CompositeReq reqs={self.reqs!r}>"

    # Convert all sub requirements from 
    def inflate(self, university: 'university.University') -> Optional['courseReq.CourseReq']:
        new_reqs: List['courseReq.CourseReq'] = []
        for req in self.reqs:
            new = req.inflate(university)
            if new:
                new_reqs.append(new)
            # ELSE ERROR
        self.reqs = new_reqs
        return self

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    @abstractmethod
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False, excl: bool=False) -> List[str]:
        pass
