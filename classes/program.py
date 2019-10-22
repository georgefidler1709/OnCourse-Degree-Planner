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

import typing
List = typing.List

import course
import courseReq
import degree

Course = course.Course
CourseReq = courseReq.CourseReq
Degree = degree.Degree

class Program(object):

    def __init__(self, degree: Degree, coursesTaken: List[Course]):
        self.degree = degree # Degree
        self.courses = coursesTaken # <List>CourseEnrollment

    @property
    def coursesTaken(self) -> List[CourseEnrollment]:
        return self.courses

    def addCourse(self, course: Course, term: String) -> None:
        enrollment = CourseEnrollment(course, term)
        self.courses.append(enrollment)

    def removeCourse(self, course: CourseEnrollment) -> None:
        self.courses.remove(course)

    def get_outstanding_reqs(self) -> List[CourseReq]:
        return self.degree.get_requirements(self.courses)

