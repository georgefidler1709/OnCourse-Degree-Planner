"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

maxDegreeReq.py
Requirement to fulfill a maximum of a particular count of uoc from a filtered
list of courses.

[MORE INFO ABOUT CLASS]
"""

from typing import List, Optional, Tuple

from . import degreeReq, courseFilter, program, course, degree

class MaxDegreeReq(degreeReq.DegreeReq):

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    def fulfilled(self, courses: List['course.Course'], degree: 'degree.Degree') -> bool:
        rem, _ = self.remaining(courses, degree)
        return rem >= 0

    # Input: a degree and a list of courses
    # Return: number of units remaining to complete this requirement
    def remaining(self, courses: Optional[List['course.Course']],
            degree: Optional['degree.Degree']) -> Tuple[int, List['course.Course']]:
        if not courses or not degree:
            return (self.uoc, [])

        if self.filter is None:
            # Overall requirement, so accept all courses and don't do anything to matching courses
            units = 0
            for c in courses:
                units += c.units
            return (self.uoc - units, [])

        units = 0
        for c in courses:
            if self.filter.accepts_course(c, degree):
                units += c.units

        return (self.uoc - units, [])

