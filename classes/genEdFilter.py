"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

genEdFilter.py
A filter that matches only general education courses

[MORE INFO ABOUT CLASS]
"""

from . import course
from . import courseFilter
from . import program


class GenEdFilter(courseFilter.CourseFilter):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f"<GenEdFilter>"

    # The name of the requirement for the database
    @property
    def filter_name(self) -> str:
        return "GenEdFilter"

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: course.Course, program: program.Program) -> bool:
        pass

    # Saves the filter in the database
    # Return: the id of the filter in the database
    def save(self) -> int:
        # TODO
        pass
