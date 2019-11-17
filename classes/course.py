"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

course.py
Implementation of the Course class, which represents a course, or individual subject.
It contains a course code, course name, UoC value, offered terms, and details
concerning requirements.

[MORE INFO ABOUT CLASS]
"""

from flask import g
from typing import List, Optional, Tuple

from . import courseReq
from . import term
from . import api
from . import course
from . import program
from . import subjectReq

class Course(object):

    def __init__(self,
            subject: str,
            code: int,
            name: str,
            units: int,
            terms: List[term.Term],
            faculty: str,
            prereqs: Optional['courseReq.CourseReq']=None,
            coreqs: Optional['courseReq.CourseReq']=None,
            exclusions: Optional[List[str]]=None,
            equivalents: Optional[List[str]]=None,
            finished: bool=True):
        # figure out inputs - database or variables?
        # to be assigned:
        self.subject = subject
        self.code = code
        self.name = name
        self.units = units
        self.terms = terms
        self.faculty = faculty
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.exclusions: List[str]
        if exclusions is None:
            self.exclusions = []
        else:
            self.exclusions = exclusions

        self.equivalents: List[str]
        if equivalents is None:
            self.equivalents = []
        else:
            self.equivalents = equivalents

        self.finished = finished

    # WARNING getting hard to debug with this, restore later
    # def __repr__(self) -> str:
    #     return f"<Course subject={self.subject!r}, code={self.code!r}, name={self.name!r}, units={self.units!r}, terms={self.terms!r}, prereqs={self.prereqs!r}, coreqs={self.coreqs!r}, exclusions={self.exclusions!r}>"

    def __repr__(self) -> str:
        return f"{self.subject}{self.code}"

    def to_api(self) -> api.Course:
        return { "code": self.course_code,
                "name": self.name,
                "units": self.units,
                "terms": [term.to_api() for term in self.terms],
                "prereqs": self.prereqs.info(top_level=True) if self.prereqs else "",
                "coreqs": self.coreqs.info(top_level=True) if self.coreqs else "",
                "exclusions": "\n".join(self.exclusions),

                "equivalents": "\n".join(self.equivalents)
                }

    # returns the SUBJxxxx course code
    @property
    def course_code(self) -> str:
        return self.subject + str(self.code)

    @property
    def level(self) -> int:
        return self.code//1000

    # Returns whether this course has an offering in the given term
    def has_offering(self, term: term.Term) -> bool:
        for t in self.terms:
            if t == term:
                return True
        return False

    # Add an offering of this course in a given term
    def add_offering(self, term: term.Term) -> None:
        self.terms.append(term)

    # Add an exclusion to this course
    def add_exclusion(self, c: str):
        if self.exclusions is None:
            self.exclusions = []
        self.exclusions.append(c)

    # Add an equivalent to this course
    def add_equivalent(self, c: str) -> None:
        if self.equivalents is None:
            self.equivalents = []
        self.equivalents.append(c)

    # Possibly need to be able to modify prereqs/coreqs?
    # Later release

    # Input: The program of the student trying to take the course, and the term they're taking it in
    # Return: whether the prerequisites have been fulfilled
    def prereqs_fulfilled(self, program: 'program.Program', term: term.Term) -> bool:
        if self.prereqs is None:
            return True
        else:
            return self.prereqs.fulfilled(program, term)

    # Input: The program of the student trying to take the course, the term they're taking it in,
    # and any additional courses they are taking that term
    # Return: whether the corequisites have been fulfilled
    def coreqs_fulfilled(self, program: 'program.Program', term: term.Term) -> bool:
        if self.coreqs is None:
            return True
        else:
            return self.coreqs.fulfilled(program, term, coreq=True)

    # Input: The program of the student trying to take the course, the term they are taking it in
    # Return: whether any exclusion courses have been taken
    def excluded(self, program: 'program.Program', term: term.Term) -> bool:
        return len(self.exclusion_errors(program, term)) != 0

    # Input: The program of the student trying to take the course, the term they are taking it in
    # Return: The list of exclusion courses that have been taken
    def exclusion_errors(self, program: 'program.Program', term: term.Term) -> List[str]:
        errors = []
        for exclusion in self.exclusions:
            for enrollment in program.courses:
                if enrollment.course.course_code == exclusion:
                    errors.append(exclusion)

        return errors

    # Input: a course
    # Return: whether it is an equivalent course
    def equivalent(self, other: 'course.Course') -> bool:
        if self.equivalents is None:
            return False
        for c in self.equivalents:
            if c == other.course_code:
                return True
        return False

    def check_reqs(self, prog: 'program.Program', term: 'term.Term') -> List[Tuple[str, List[str]]]:
        errors = []
        if self.prereqs is not None:
            prereq_errors = self.prereqs.check(prog, term)
            if len(prereq_errors) > 0:
                errors.append(("Prerequisite:", prereq_errors))

        if self.coreqs is not None:
            coreq_errors = self.coreqs.check(prog, term, coreq=True)
            if len(coreq_errors) > 0:
                errors.append(("Corequisite:", coreq_errors))

        # handle exclusions
        exclusion_errors = self.exclusion_errors(prog, term)
        if len(exclusion_errors) > 0:
            errors.append(("Exclusion:", exclusion_errors))
        # min mark warnings

        return errors

    # Override comparison fucntions
    def __lt__(self, other) -> bool: # x < y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str < other_str

    def __le__(self, other) -> bool: # For x <= y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str <= other_str

    def __eq__(self, other) -> bool: # For x == y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str == other_str

    def __ne__(self, other) -> bool: # For x != y OR x <> y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str != other_str

    def __gt__(self, other) -> bool: # For x > y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str > other_str

    def __ge__(self, other) -> bool: # For x >= y
        self_str = self.subject + str(self.code)
        other_str = other.subject + str(other.code)

        return self_str >= other_str

