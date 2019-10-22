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

    def __init__(self, subject: str, code: int, name: str, units: int, terms: List[Term],
            prereqs: CourseReq, coreqs: CourseReq, exclusions: CourseReq):
        # figure out inputs - database or variables?
        # to be assigned:
        self._subject = subject
        self._code = code
        self._name = name
        self._units = units
        self._terms = terms
        self._prereqs = prereqs
        self._coreqs = coreqs
        self._exclusions = exclusions

    # returns the SUBJxxxx course code
    def courseCode(self):
        return self._subject + str(self._code)

    @property
    def name(self):
        return self._name
        
    @property
    def subject(self):
        return self._subject
    
    @property
    def level(self)
    return self._code/1000

    @property
    def units(self):
        return self._units
    
    @property
    def terms(self):
        return self._terms

    # Add an offering of this course in a given term
    def addOffering(self, term: Term) -> None:
        self._terms.append(term)

    # Possibly need to be able to modify prereqs/coreqs?
    # Later release

    # Input: The program of the student trying to take the course, and the term they're taking it in
    # Return: whether the prerequisites have been fulfilled
    def prereqsFulfilled(self, program: Program, term: int) -> bool:
        return self._prereqs.fulfilled(program, term, coreq=False)

    # Input: The program of the student trying to take the course, the term they're taking it in,
    # and any additional courses they are taking that term
    # Return: whether the corequisites have been fulfilled
    def coreqsFulfilled(self, program: Program, term: int, additionalCourses: List[Course]) -> bool:
        return self._coreqs.fulfilled(program, term, additionalCourses, coreq=True)

    # THINK about corequisites - what if prerequisite OR corequisite?

    # Input: The program of the student trying to take the course, the term they are taking it in,
    # and any additional courses they are taking that term
    # Return: whether any exclusion courses have been taken
    def excluded(self, program: Program, term: int, additionalCourses: List[Course]) -> bool:
        return self._exclusions.fulfilled(program, term, additionalCourses, coreq=True)


