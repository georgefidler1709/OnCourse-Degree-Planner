"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

levelFilter.py
Implementation of the LevelFilter class, which allows courses to be filtered
based on course level.

[MORE INFO ABOUT CLASS]
"""
from abc import abstractmethod

import course
import program
from courseFilter import CourseFilter

class LevelFilter(CourseFilter):

    def __init__(self, level: int):
        self.level = level

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    @abstractmethod
    def accepts_course(self, course: 'course.Course', program: 'program.Program') -> bool:
        return course.level == self.level
