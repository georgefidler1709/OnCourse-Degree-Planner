"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the Program class, which represents a specific program of
study.

[MORE INFO ABOUT CLASS]
"""

from typing import List

from course import Course
from courseReq import CourseReq
from degree import Degree

class Program(object):

    def __init__(self, degree: Degree, coursesTaken: List[Course]):
        self.degree = degree # Degree
        self.courses = coursesTaken # <List>CourseEnrollment

    @property
    def courses_taken(self) -> List[Course]:
        return self.courses

    def add_course(self, course: Course) -> None:
        self.courses.append(course)

    def remove_course(self, course: Course) -> None:
        self.courses.remove(course)

    def get_outstanding_reqs(self) -> List[CourseReq]:
        return self.degree.get_requirements(self.courses)

