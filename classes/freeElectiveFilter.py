"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

freeElectiveFilter.py
A filter that matches free electives (should be anything)

[MORE INFO ABOUT CLASS]
"""

import course
import courseFilter
import program

Course = course.Course
CourseFilter = courseFilter.CourseFilter
Program = program.Program

class FieldFilter(CourseFilter):

    def __init__(self):
        super().__init__()

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: Course, program: Program) -> bool:
        return True
