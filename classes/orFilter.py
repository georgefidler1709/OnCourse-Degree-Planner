"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

orFilter.py
A filter that allows courses that match any of the provided filters

[MORE INFO ABOUT CLASS]
"""

from typing import List

from course import Course
from courseFilter import CourseFilter
from program import Program

class FieldFilter(CourseFilter):

    def __init__(self, filters: List[CourseFilter]):
        super().__init__()
        self.filters = filters

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def acceptsCourse(self, course: Course, program: Program) -> bool:
        # make an iterable where element at a position is True if the filter at that position accepts
        individualAcceptance = map(lambda x: x.acceptsCourse(course, program), self.filters)

        # accept if any of the filters accepts
        return any(individualAcceptance)
