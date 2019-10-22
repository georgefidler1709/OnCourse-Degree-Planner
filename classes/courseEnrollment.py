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

    def __init__(self, course: Course, term: Term):
        self._course = course
        self._term = term

    @property
    def course(self):
        return self._course

    @property
    def term(self):
        return self.Term

    def courseCode(self) -> str:
        return self._course.courseCode()

    def courseName(self) -> str:
        return self._course.name

    def units(self) -> int:
        return self._course.units

