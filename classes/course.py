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

from typing import List

from courseReq import CourseReq
from program import Program

class Course(object):

    def __init__(self, subject: str, code: int, name: str, units: int, terms: List[int],
            prereqs: CourseReq, coreqs: CourseReq, exclusions: CourseReq):
        # figure out inputs - database or variables?
        # to be assigned:
        self.subject = subject
        self.code = code
        self.name = name
        self.units = units
        self.terms = terms
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.exclusions = exclusions

    @property
    def courseCode(self):
        return self.subject + str(self.code)

    @property
    def subjectArea(self):
        return self.subject
    
    @property
    def level(self)
    return self.code/1000

    @property
    def units(self):
        return self.units
    
    @property
    def terms(self):
        return self.terms

    # Add an offering of this course in a given term
    def addOffering(self, term: int) -> None:
        self.terms.append(term)

    # Possibly need to be able to modify prereqs/coreqs?
    # Later release

    # Input: The program of the student trying to take the course, and the term they're taking it in
    # Return: whether the prerequisites have been fulfilled
    def prereqsFulfilled(self, program: Program, term: int) -> bool:
        return self.prereqs.fulfilled(program, term, coreq=False)

    # Input: The program of the student trying to take the course, the term they're taking it in,
    # and any additional courses they are taking that term
    # Return: whether the corequisites have been fulfilled
    def coreqsFulfilled(self, program: Program, term: int, additionalCourses: List[Course]) -> bool:
        return self.coreqs.fulfilled(program, term, additionalCourses, coreq=True)

    # THINK about corequisites - what if prerequisite OR corequisite?

    # Input: The program of the student trying to take the course, the term they are taking it in,
    # and any additional courses they are taking that term
    # Return: whether any exclusion courses have been taken
    def excluded(self, program: Program, term: int, additionalCourses: List[Course]) -> bool:
        return self.exclusions.fulfilled(program, term, additionalCourses, coreq=True)


