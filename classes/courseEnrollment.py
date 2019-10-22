"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseEnrollment.py
Implementation of the CourseEnrollment class, which represents an enrollment in
a course. This contains the course enrolled in and the term in which the course
will be taken.

[MORE INFO ABOUT CLASS]
"""

from course import Course

class CourseEnrollment(object):

    def __init__(self, course: Course, term: int):
        self.course = course
        self.term = term

    @property
    def courseCode(self) -> str:
        return self.course.code

    @property
    def courseName(self) -> str:
        return self.course.name

    @property
    def uocCount(self) -> int:
        return self.course.units
