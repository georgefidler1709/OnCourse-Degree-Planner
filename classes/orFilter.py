"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

orFilter.py
A filter that allows courses that match any of the provided filters

[MORE INFO ABOUT CLASS]
"""

import typing
List = typing.List

import course
import courseFilter
import program

Course = course.Course
CourseFilter = courseFilter.CourseFilter
Program = program.Program

class FieldFilter(CourseFilter):

    def __init__(self, filters: List[CourseFilter]):
        super().__init__()
        self.filters = filters

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: Course, program: Program) -> bool:
        # make an iterable where element at a position is True if the filter at that position accepts
        individual_acceptance = map(lambda x: x.accepts_course(course, program), self.filters)

        # accept if any of the filters accepts
        return any(individual_acceptance)
