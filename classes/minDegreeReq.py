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

from typing import List, Optional
from . import degreeReq, courseFilter, program, course, degree

class MinDegreeReq(degreeReq.DegreeReq):

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    def fulfilled(self, courses: List['course.Course'], degree: 'degree.Degree') -> bool:
        return self.remaining(courses, degree) == 0

    # Input: a degree and a list of courses
    # Return: number of units remaining to complete this requirement
    # Note: Deletes matching courses from list!
    def remaining(self, courses: Optional[List['course.Course']],
            degree: Optional['degree.Degree']) -> int:
        if not courses or not degree:
            return self.uoc

        units = 0
        matching_courses = []
        for c in courses:
            if self.filter.accepts_course(c, degree):
                units += c.units
                matching_courses.append(c)
                if units == self.uoc:
                    break

        # Remove matching courses from import course list
        # Only if this 
        for c in matching_courses:
            courses.remove(c)

        return self.uoc - units