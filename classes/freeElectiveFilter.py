"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

freeElectiveFilter.py
A filter that matches free electives (should be anything)

[MORE INFO ABOUT CLASS]
"""

import course
import courseFilter
import degree


class FieldFilter(courseFilter.CourseFilter):

    def __init__(self):
        super().__init__()

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: course.Course, degree: degree.Degree) -> bool:
        return True
