"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degreeReq.py
Implementation of the DegreeReq class which specifies a degree requirement.
These requirements take the form of a count of units from a particular
filter of courses.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from . import courseFilter
from . import program
from . import course
from . import degree


class DegreeReq(ABC):

    def __init__(self, filter: 'courseFilter.CourseFilter', uoc: int):
        # input as separate variables? or some other format
        self.uoc = uoc
        self.filter = filter
        super().__init__()

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    @abstractmethod
    def fulfilled(self, courses: List['course.Course'], deg: 'degree.Degree') -> bool:
        pass

    # Return whether this is a core requirement
    def core_requirement(self) -> bool:
        return self.filter.core

    # Saves the requirement in the database
    # Return: the id of the filter in the database
    def save(self):
        return self.filter.save()
