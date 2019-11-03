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

from typing import List
from . import degreeReq, courseFilter, program, course, degree

class MaxDegreeReq(degreeReq.DegreeReq):

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    def fulfilled(self, program:'program.Program') -> bool:
        units = 0
        for c in program.courses:
            if self.filter.accepts_course(c.course, program.degree):
                units += c.units()
        return units < self.uoc


