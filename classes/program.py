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
import courseReq
import degree


class Program(object):

    def __init__(self, degree: degree.Degree, coursesTaken: List[course.Course]):
        self.degree = degree # degree.Degree
        self.courses = coursesTaken # <List>CourseEnrollment

    @property
    def courses_taken(self) -> List[course.Course]:
        return self.courses

    def add_course(self, course: course.Course) -> None:
        self.courses.append(course)

    def remove_course(self, course: course.Course) -> None:
        self.courses.remove(course)

    def get_outstanding_reqs(self) -> List[courseReq.CourseReq]:
        return self.degree.get_requirements(self.courses)

