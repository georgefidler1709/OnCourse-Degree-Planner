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


class MaxDegreeReq(DegreeReq):

    def __init__(self, filter: 'courseFilter.CourseFilter', uoc: int):
        super().__init__()

    # Input: a program of study
    # Return: whether this prorgram would fulfil this degree requirement
    def fulfilled(self, courses: List['course.Course']) -> bool:
        units = 0
        for course in courses:
            if self.filter.accepts_course(course, program):
                units += course.units
        return units < self.uoc


