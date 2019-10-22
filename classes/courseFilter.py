"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseFilter.py
Implementation of the CourseFilter class, an abstract class which collects types
of filters for courses.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from flask import g
from typing import List

import course
import program


class CourseFilter(ABC):

    def __init__(self):
        pass

    # The name of the requirement for the database
    @property
    @abstractmethod
    def filter_name(self) -> str:
        return "GenericRequirement"

    # The id of the requirement for the database
    @property
    def filter_id(self) -> int:
        return g.db.execute('select id from CourseFilterTypes where name = ?', self.filter_name)



    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    @abstractmethod
    def accepts_course(self, course: 'course.Course', program: 'program.Program') -> bool:
        pass

    # Saves the filter in the database
    # Return: the id of the filter in the database
    @abstractmethod
    def save(self) -> int:
        g.db.execute('''insert into CourseFilters(type_id) values(?)''',
                self.filter_id)

        return g.db.lastrowid
