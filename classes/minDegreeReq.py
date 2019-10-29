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

from typing import List
import degreeReq
import degree
import program
import courseFilter
import course

class MinDegreeReq(degreeReq.DegreeReq):

    def __init__(self, filter: 'courseFilter.CourseFilter', uoc: int):
        super().__init__(filter, uoc)

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    def fulfilled(self, courses: List['course.Course'], deg: 'degree.Degree') -> bool:
        units = 0
        for c in courses:
            if self.filter.accepts_course(c, deg):
                units += c.units
        
        return units >= self.uoc
    
    # Input: a degree and a list of courses
    # Return: number of units remaining to complete this requirement
    def remaining(self, program: 'program.Program'):
        units = 0
        for course in program.courses:
            if self.filter.accepts_course(course, program):
                units += course.units
        return self.uoc - units