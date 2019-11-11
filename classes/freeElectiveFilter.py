"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

freeElectiveFilter.py
A filter that matches free electives (should be anything)

[MORE INFO ABOUT CLASS]
"""

from . import course
from . import courseFilter
from . import degree


class FreeElectiveFilter(courseFilter.CourseFilter):

    def __init__(self):
        super().__init__()

    def __repr__(self) -> str:
        return f"<FreeElectiveFilter>"

    def info(self) -> str:
        return "Any course"

    @property
    def core(self) -> bool:
        return False

    @property
    def field_filter(self) -> bool:
        return False

    # The name of the requirement for the database
    @property
    def filter_name(self) -> str:
        return "FreeElectiveFilter"

    @property
    def info(self) -> str:
        return 'Any free elective'

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        return True

    # Saves the filter in the database
    # Return: the id of the filter in the database
    def save(self) -> int:
        # TODO
        pass
