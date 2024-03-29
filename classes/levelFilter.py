'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

levelFilter.py
Implementation of the LevelFilter class, which allows courses to be filtered
based on course level.
'''

from abc import abstractmethod

from . import course, degree
from .courseFilter import CourseFilter


class LevelFilter(CourseFilter):

    def __init__(self, level: int):
        self.level = level

    def __repr__(self) -> str:
        return f'<LevelFilter level={self.level!r}>'

    @property
    def filter_name(self) -> str:
        return 'LevelFilter'

    @property
    def info(self) -> str:
        return f'level {self.level}'

    @property
    def core(self) -> bool:
        return False

    @property
    def field_filter(self) -> bool:
        return False

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        return course.level == self.level
