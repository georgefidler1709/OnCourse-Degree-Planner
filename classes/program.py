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

from typing import List, Optional, Dict

from . import course
from . import courseEnrollment
from . import degree
from . import degreeReq
from . import term
from . import api


class Program(object):

    def __init__(self, degree: 'degree.Degree', coursesTaken: List['courseEnrollment.CourseEnrollment']):
        self.degree = degree # degree.Degree
        self.courses = coursesTaken # <List>CourseEnrollments

    # Input: a course
    # Return: Whether there is already an enrollment for this course in this term
    def enrolled(self, course: 'course.Course') -> bool:
        for enrollment in self.courses:
            if enrollment.course == course:
                return True
        return False

    # Input: a course
    # Return: term in which that course is taken
    def term_taken(self, course: 'course.Course') -> Optional['term.Term']:
        for enrollment in self.courses:
            if enrollment.course == course:
                return enrollment.term
        return None

    def __repr__(self) -> str:
        return f"<Program degree={self.degree!r}, courses={self.courses!r}>"

    def add_course(self, course: 'course.Course', term: term.Term) -> None:
        if self.enrolled(course):
            return
        enrollment = courseEnrollment.CourseEnrollment(course, term)
        self.courses.append(enrollment)

    def remove_course(self, course: 'courseEnrollment.CourseEnrollment') -> None:
        self.courses.remove(course)

    def unit_count(self, term: 'term.Term') -> int:
        units = 0
        for enrollment in self.courses:
            if enrollment.term == term:
                units += enrollment.course.units
        return units

    def get_outstanding_reqs(self) -> Dict[('degreeReq.DegreeReq', int)]:
        return self.degree.get_requirements(self)

    def to_api(self) -> api.Program:
        return {'id': self.degree.num_code, 
                'name': self.degree.name,
                'year': self.degree.year,
                'duration': self.degree.duration,
                'enrollments': [course.to_api() for course in self.courses]};
