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
import typing
List = typing.List

import course
import program

Course = course.Course
Program = program.Program

class CourseFilter(ABC):

    def __init__(self):
        pass

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    @abstractmethod
    def accepts_course(self, course: Course, program: Program) -> bool:
        pass
