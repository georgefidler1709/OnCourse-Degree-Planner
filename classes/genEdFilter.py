'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

genEdFilter.py
A filter that matches only general education courses
'''

from . import course
from . import courseFilter
from . import degree

class GenEdFilter(courseFilter.CourseFilter):

    def __init__(self):
        super().__init__()

    def __repr__(self):
        return f'<GenEdFilter>'

    @property
    def core(self) -> bool:
        return False

    @property
    def field_filter(self) -> bool:
        return False

    # The name of the requirement for the database
    @property
    def filter_name(self) -> str:
        return 'GenEdFilter'

    @property
    def simple_name(self) -> str:
        return 'General education'

    @property
    def info(self) -> str:
        # TODO can add the URL here or as a button on front-end
        return 'Any general education course'

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        return course.faculty != degree.faculty
