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

    def __init__(self, degree: Degree, coursesTaken: List[CourseEnrollment]):
        self._degree = degree # Degree
        self._courses = coursesTaken # <List>CourseEnrollment

    @property
    def coursesTaken(self) -> List[CourseEnrollment]:
        return self._courses

    def addCourse(self, course: Course, term: Term) -> None:
        enrollment = CourseEnrollment(course, term)
        self._courses.append(enrollment)

    def removeCourse(self, course: CourseEnrollment) -> None:
        self._courses.remove(course)

    def getOutstandingReqs(self) -> List[CourseReq]:
        return self._degree.getRequirements(self._courses)

