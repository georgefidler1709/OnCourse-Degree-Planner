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
        return self.remaining(courses, degree) <= 0

    # Input: a degree and a list of courses
    # Return: number of units remaining to complete this requirement
    # Note: Deletes matching courses from list!
    def remaining(self, courses: Optional[List['course.Course']],
            degree: Optional['degree.Degree']) -> int:
        if not courses or not degree:
            return self.uoc

        if self.filter is None:
            # Overall requirement, so accept all courses and don't do anything to matching courses
            units = 0
            for c in courses:
                units += c.units
            return self.uoc - units

        # print("------------ courses -----------------")
        # print(courses)
        # print("--------------------------------")

        units = 0
        matching_courses = []
        for c in courses:
            if self.filter.accepts_course(c, degree):
                units += c.units
                matching_courses.append(c)
                if units == self.uoc:
                    break

        # print("====== matching courses in MinDegreeReq.remaining() ======")
        # print(matching_courses)
        # print(f"----> units = {units}")
        # print("=====================================")

        # I think this bug is fixed?
        # bug is that the matching courses are being found
        # but not shown on the other side. Return 2 things instead?
        # courses.remove() not working or not being added to dict

        # Remove matching courses from import course list
        # Only if this 
        for c in matching_courses:
            courses.remove(c)
        # print("---------- courses ---------")
        # print(courses)
        # print("----------------------------")

        return self.uoc - units
