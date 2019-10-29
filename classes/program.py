"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the Program class, which represents a specific program of
study.

[MORE INFO ABOUT CLASS]
"""

from typing import List

import course
import courseEnrollment
import degree
import degreeReq
import term


class Program(object):

    def __init__(self, degree: 'degree.Degree', coursesTaken: List['courseEnrollment.CourseEnrollment']):
        self.degree = degree # degree.Degree
        self.courses = coursesTaken # <List>CourseEnrollments

    def add_course(self, course: 'course.Course', term: term.Term) -> None:
        enrollment = courseEnrollment.CourseEnrollment(course, term)
        self.courses.append(enrollment)

    def remove_course(self, course: 'courseEnrollment.CourseEnrollment') -> None:
        self.courses.remove(course)

    def get_outstanding_reqs(self) -> List['degreeReq.DegreeReq']:
        return self.degree.get_requirements(self)

    def unit_count(self, term: 'term.Term') -> int:
        units = 0
        for enrollment in self.courses:
            if enrollment.term == term:
                units += enrollment.course.units
        return units


