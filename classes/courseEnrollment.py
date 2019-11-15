"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseEnrollment.py
Implementation of the CourseEnrollment class, which represents an enrollment in
a course. This contains the course enrolled in and the term in which the course
will be taken.

[MORE INFO ABOUT CLASS]
"""

from . import course
from . import term
from . import api

class CourseEnrollment(object):

    def __init__(self, course: 'course.Course', term: term.Term):
        self.course = course
        self.term = term

    def __repr__(self) -> str:
        return f"<CourseEnrollment course={self.course!r}, term={self.term!r}>"

    def course_code(self) -> str:
        return self.course.course_code

    def course_name(self) -> str:
        return self.course.name

    def units(self) -> int:
        return self.course.units

    # override equality
    def __eq__(self, other) -> bool: # For x == y
        if (isinstance(other, CourseEnrollment) and 
            self.course == other.course and self.term == other.term):
            return True
        else:
            return False
