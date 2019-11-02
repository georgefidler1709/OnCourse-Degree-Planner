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
from typing import List

import course
import term
import program

class CourseReq(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return f"<CourseReq>"

    # The name of the requirement for the database
    @property
    # @abstractmethod
    def requirement_name(self) -> str:
        return "GenericRequirement"

    # The id of the requirement for the database
    @property
    def requirement_id(self) -> int:
        return g.db.execute('select id from CourseRequirementTypes where name = ?',
                self.requirement_name)

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    # coreq set to False, if true then terms allowed include input term
    @abstractmethod
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False) -> bool:
        pass

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    # @abstractmethod
    def save(self) -> int:
        g.db.execute('''insert into CourseRequirements(type_id) values(?)''',
                self.requirement_id)

        return g.db.lastrowid
