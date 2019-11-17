"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseReq.py
Implementation of the CourseReq class, an abstract class which collects types
of course requirements.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from flask import g
from typing import List, Optional

from . import course
from . import term
from . import program

class CourseReq(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return f"<CourseReq>"

    # Get info for the requirement, for displaying in information for the course
    @abstractmethod
    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        pass

    # The name of the requirement for the database
    @property
    # @abstractmethod
    def requirement_name(self) -> str:
        return "GenericRequirement"

    @abstractmethod
    def inflate(self, university: 'university.University') -> Optional['CourseReq']:
        pass

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    @abstractmethod
    def check(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False, excl: bool=False) -> List[str]:
        pass

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    # coreq set to False, if true then terms allowed include input term
    # ex set to False, if true then this is an exclusion requirement
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False, excl: bool=False) -> bool:
        if excl:
            return len(self.check(program, term, coreq, excl)) == 0
        else:
            return len(self.check(program, term, coreq)) == 0

# Imports that were causing circular dependency issues at the bottom
from . import university
