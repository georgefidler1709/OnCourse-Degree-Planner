"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

fieldFilter.py
A filter that matches only courses in a specific field

[MORE INFO ABOUT CLASS]
"""

import course
import courseFilter
import program


class FieldFilter(courseFilter.CourseFilter):

    def __init__(self, field: str):
        super().__init__()
        self.field = field

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: course.Course, program: program.Program) -> bool:
        return course.subject == self.field
