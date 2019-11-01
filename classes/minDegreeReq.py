"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

minDegreeReq.py
Requirement to fulfill a minimum of a particular count of uoc from a filtered
list of courses.

[MORE INFO ABOUT CLASS]
"""

from . import degreeReq
from . import program
from . import courseFilter
from . import course

class MinDegreeReq(degreeReq.DegreeReq):

    def __init__(self, filter: 'courseFilter.CourseFilter', uoc: int):
        super().__init__(filter, uoc)

    # Input: a program of study
    # Return: whether this prorgram would fulfil this degree requirement
    def fulfilled(self, prog: 'program.Program') -> bool:
        units = 0
        for course in courses:
            if self.filter.accepts_course(course, prog):
                units += course.units
        return units >= self.uoc
    
    # Input: a program of study
    # Return: whether this prorgram would fulfil this degree requirement
    # Input: a program of study
    # Return: number of units remaining to complete this requirement
    def remaining(self, program: 'program.Program'):
        units = 0
        for course in program.courses:
            if self.filter.accepts_course(course, program):
                units += course.units
        return self.uoc - units
