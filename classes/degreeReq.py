"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degreeReq.py
Implementation of the DegreeReq class which specifies a degree requirement.
These requirements take the form of a count of units from a particular
filter of courses.

[MORE INFO ABOUT CLASS]
"""

from typing import Optional

from . import courseFilter
from . import program


class DegreeReq(object):

    def __init__(self, filter: 'courseFilter.CourseFilter', uoc: int):
        # input as separate variables? or some other format
        self.uoc = uoc
        self.filter = filter
        super().__init__()

    # Input: a program of study
    # Return: whether this prorgram would fulfil this degree requirement
    def fulfilled(self, program: Optional['program.Program']) -> bool:
        if program is None:
            # No degree requirement should be fulfilled by default
            return False

        units = 0

        for enrollment in program.courses:
            course = enrollment.course
            if self.filter.accepts_course(course, program):
                units += course.units
        return units >= self.uoc

    # Input: a program of study
    # Return: number of units remaining to complete this requirement
    def remaining(self, program: Optional['program.Program']):
        if program is None:
            return self.uoc

        units = 0
        for enrollment in program.courses:
            course = enrollment.course
            if self.filter.accepts_course(course, program):
                units += course.units
        return self.uoc - units

    # Saves the requirement in the database
    # Return: the id of the filter in the database
    def save(self):
        return self.filter.save()
