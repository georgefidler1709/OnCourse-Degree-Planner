"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseReq.py
Implementation of the CourseReq class, an abstract class which collects types
of course requirements.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from flask import g
from typing import List

from course import Course
from program import Program

class CourseReq(ABC):

    def __init__(self):
        super().__init__()

    # The name of the requirement for the database
    @abstractmethod
    @property
    def requirement_name(self) -> str:
        return "GenericRequirement"

    # The id of the requirement for the database
    @property
    def requirement_id(self) -> int:
        return g.db.execute('select id from CourseRequirementTypes where name = ?',
                self.requirement_name)

        # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    # coreq set to False, if true then terms allowed include input term
    @abstractmethod
    def fulfilled(self, program: Program, term: int,
            additional_courses: List[Course]=[], coreq: bool=False) -> bool:
        pass

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    @abstractmethod
    def save(self) -> int:
        g.db.execute('''insert into CourseRequirementTypes(type_id) values(?)''',
                self.requirement_id)

        return g.db.lastrowid
