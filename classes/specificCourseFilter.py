"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

specificCourseFilter
A filter that matches only one course

[MORE INFO ABOUT CLASS]
"""

import course
import courseFilter
import program

Course = course.Course
CourseFilter = courseFilter.CourseFilter
Program = program.Program

class SpecificCourseFilter(CourseFilter):

    def __init__(self, course: Course):
        super().__init__()
        self.course = course

    # Input: Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: Course, program: Program) -> bool:
        return course == self.course
