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

from . import course
from . import degree

class CourseFilter(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def __repr__(self) -> str:
        return f"<CourseFilter>"

    # Get info for the filter, for displaying in information for the degree
    @abstractmethod
    def info(self) -> str:
        pass

    # The name of the requirement for the database
    @property
    @abstractmethod
    def filter_name(self) -> str:
        return "GenericFilter"

    # gets rid of "Filter" in self.filter_name
    @property
    def simple_name(self) -> str:
        name = self.filter_name
        if "Filter" in name:
            name = name.split("Filter")[0]
        return name

    # returns information about the filter in a string form
    # for easy displaying on front-end
    # see individual filters for information it needs to pass
    @property
    def info(self) -> str:
        return 'some info about the filter'

    # The id of the requirement for the database
    @property
    def filter_id(self) -> int:
        return g.db.execute('select id from CourseFilterTypes where name = ?', self.filter_name)

    # Returns whether this filters specific courses
    @property
    @abstractmethod
    def core(self) -> bool:
        pass

    # Returns whether this filters based on field
    @property
    @abstractmethod
    def field_filter(self) -> bool:
        pass

    # Input: Course, program the student is enrolled in,
    # eq to indicate whether equivalent courses should be considered
    # Return: Whether this course matches the filter
    @abstractmethod
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        pass

    # Saves the filter in the database
    # Return: the id of the filter in the database
    #@abstractmethod
    def save(self) -> int:
        g.db.execute('''insert into CourseFilters(type_id) values(?)''',
                self.filter_id)

        return g.db.lastrowid
