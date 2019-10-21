"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

university.py
Implementation of the University class which is a database of courses and programs

[MORE INFO ABOUT CLASS]
"""

from typing import List

from degree import Degree
from course import Course
from courseFilter import CourseFilter

class University(object):

    def __init__(self, degrees: List[Degree], courses: List[Course]):
        # need to decide how degree/course details passed in
        # unpack and create Degree and Course objects
        self.degrees = degrees
        self.courses = courses

    # Input: degree letter code (eg. COMPA1)
    # Return: corresponding Degree object
    def findDegreeByLetterCode(self, letter_code: str) -> Degree:
        # TODO
        pass

    # Input: degree numerical code (eg. 3778)
    # Return: corresponding Degree object
    def findDegreeByNumberCode(self, numeric_code: int) -> Degree:
        # TODO
        pass

    # Input: course code (eg. COMP1511)
    # Return: corresponding Course object from self.courses
    def findCourse(self, code: str) -> Course:
        # TODO
        pass

    # Input: A filter string [ITEMISE THESE HERE]
    # Return: List of courses that match the requested filter
    def filterCourses(self, filter: CourseFilter) -> List[Course]:
        # TODO
        pass
