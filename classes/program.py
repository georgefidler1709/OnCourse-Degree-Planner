"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the Program class, which represents a specific program of
study.

[MORE INFO ABOUT CLASS]
"""

# imports go here

class Program(object):

    def __init__(self, degree, coursesTaken):
        self.degree = degree # Degree
        self.courses = courses # <List>CourseEnrollment

    @property
    def degree(self):
        return self.degree

    @property
    def coursesTaken(self):
        return self.courses

    def addCourse(self, course):
        courses.add(course)

    def removeCourse(self, course):
        courses.remove(course)

    def getOutstandingReqs(self):
        return degree.getRequirements(courses)

