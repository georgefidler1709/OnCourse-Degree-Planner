"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

genEdFilter.py
A filter that matches only general education courses

[MORE INFO ABOUT CLASS]
"""

import course
import courseFilter
import program


class GenEdFilter(courseFilter.CourseFilter):

    def __init__(self):
        super().__init__()

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: course.Course, program: program.Program) -> bool:
        pass
