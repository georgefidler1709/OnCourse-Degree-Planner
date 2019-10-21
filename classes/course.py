"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

course.py
Implementation of the Course class, which represents a course, or individual subject.
It contains a course code, course name, UoC value, offered terms, and details
concerning requirements.

[MORE INFO ABOUT CLASS]
"""

class Course(object):

    def __init__(self):
        # figure out inputs - database or variables?
        # to be assigned:
        # self.code =
        # self.name =
        # self.units =
        # self.terms
        # self.prereqs # CourseRequirement
        # self.coreqs #CourseRequirement
        # self.exclusions # <List>Course

    @property
    def code(self):
        return self.code
    
    @property
    def name(self):
        return self.name

    @property
    def units(self):
        return self.units
    
    @property
    def terms(self):
        return self.terms

    # Add an offering of this course in a given term
    def addOffering(self, term):
        terms.add(term)

    # Possibly need to be able to modify prereqs/coreqs?
    # Later release

    # Input: List of CourseEnrollments and a proposed term for enrollment
    # Return: whether the prerequisites have been fulfilled
    def prereqsFulfilled(self, term, courses):
        return prereqs.fulfilled(courses, term)

    # THINK about corequisites - what if prerequisite OR corequisite?

    # Input: list of CourseEnrollments
    # Return: whether any exclusion courses have been taken
    def excluded(self, courses):
        # TODO


