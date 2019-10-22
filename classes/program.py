"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the program.Program class, which represents a specific program of
study.

[MORE INFO ABOUT CLASS]
"""

from typing import List

import course
import courseEnrollment
import courseReq
import degree
import term


class Program(object):

    def __init__(self, degree: degree.Degree, coursesTaken: List[courseEnrollment.CourseEnrollment]):
        self.degree = degree # degree.Degree
        self.courses = coursesTaken # <List>CourseEnrollment

    @property
    def coursesTaken(self) -> List[courseEnrollment.CourseEnrollment]:
        return self.courses

    def addCourse(self, course: course.Course, term: term.Term) -> None:
        enrollment = courseEnrollment.CourseEnrollment(course, term)
        self.courses.append(enrollment)

    def removeCourse(self, course: courseEnrollment.CourseEnrollment) -> None:
        self.courses.remove(course)

    def get_outstanding_reqs(self) -> List[courseReq.CourseReq]:
        return self.degree.getRequirements(self.courses)

