"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

university.py
Implementation of the University class which is a database of courses and programs

[MORE INFO ABOUT CLASS]
"""

from typing import List

import degree
import course
import courseFilter


class University(object):

    def __init__(self, degrees: List['degree.Degree'], courses: List['course.Course']):
        # need to decide how degree/course details passed in
        # unpack and create degree.Degree and course.Course objects
        self.degrees = degrees
        self.courses = courses

    # Input: degree letter code (eg. COMPA1)
    # Return: corresponding degree.Degree object
    def find_degree_alpha_code(self, letter_code: str) -> 'degree.Degree':
        # TODO
        pass

    # Input: degree numerical code (eg. 3778)
    # Return: corresponding degree.Degree object
    def find_degree_number_code(self, numeric_code: int) -> 'degree.Degree':
        # TODO
        pass

    # Input: course code (eg. COMP1511)
    # Return: corresponding Course object from self.courses
    def find_course(self, code: str) -> 'course.Course':
        # TODO
        pass

    # Input: A filter string [ITEMISE THESE HERE]
    # Return: List of courses that match the requested filter
    def filter_courses(self, filter: 'courseFilter.CourseFilter') -> List['course.Course']:
        # TODO
        pass
