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
from typing import List

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

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    @abstractmethod
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False, ex: bool=False) -> bool:
        pass
