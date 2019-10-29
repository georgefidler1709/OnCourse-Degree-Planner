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
from typing import List, Optional

from . import courseReq
from . import program
from . import term

class Course(object):

    def __init__(self, subject: str, code: int, name: str, units: int, terms: List[term.Term],
            prereqs: Optional['courseReq.CourseReq'], coreqs: Optional['courseReq.CourseReq'],
            exclusions: Optional['courseReq.CourseReq']):
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

    def __repr__(self) -> str:
        return f"<Course subject={self.subject!r}, code={self.code!r}, name={self.name!r}, units={self.units!r}, terms={self.terms!r}, prereqs={self.prereqs!r}, coreqs={self.coreqs!r}, exclusions={self.exclusions!r}>"


    # returns the SUBJxxxx course code
    @property
    def course_code(self) -> str:
        return self.subject + str(self.code)

    @property
    def level(self) -> int:
        return self.code//1000

    # Add an offering of this course in a given term
    def add_offering(self, term: term.Term) -> None:
        self.terms.append(term)

    # Possibly need to be able to modify prereqs/coreqs?
    # Later release

    # Input: The program of the student trying to take the course, and the term they're taking it in
    # Return: whether the prerequisites have been fulfilled
    def prereqs_fulfilled(self, program: 'program.Program', term: term.Term) -> bool:
        if self.prereqs is None:
            return True
        else:
            return self.prereqs.fulfilled(program, term, coreq=False)

    # Input: The program of the student trying to take the course, the term they're taking it in,
    # and any additional courses they are taking that term
    # Return: whether the corequisites have been fulfilled
    def coreqs_fulfilled(self, program: 'program.Program', term: term.Term) -> bool:
        if self.coreqs is None:
            return True
        else:
            return self.coreqs.fulfilled(program, term, coreq=True)

    # THINK about corequisites - what if prerequisite OR corequisite?

    # Input: The program of the student trying to take the course, the term they are taking it in
    # Return: whether any exclusion courses have been taken
    def excluded(self, program: 'program.Program', term: term.Term) -> bool:
        if self.exclusions is None:
            return False
        else:
            return self.exclusions.fulfilled(program, term, coreq=True)

    # Saves the course in the database
    # Return: the id of the course
    def save(self) -> int:
        if self.prereqs is None:
            prereq_id = None
        else:
            prereq_id = self.prereqs.save()

        if self.coreqs is None:
            coreq_id = None
        else:
            coreq_id = self.coreqs.save()

        if self.exclusions is None:
            exclusions_id = None
        else:
            exclusions_id = self.exclusions.save()

        # save the course itself
        g.db.execute('''insert into Courses(letter_code, number_code, level, name, units, prereq,
        coreq, exclusion) values (?, ?, ?, ?, ?, ?, ?)''',
        self.subject, self.code, self.level, self.name, self.units, prereq_id, coreq_id,
        exclusions_id)

        course_id = g.db.lastrowid

        # save the offerings of the course
        for term in self.terms:
            term.save()

            g.db.execute('''insert into CourseOfferings(course_id, session_year, session_term)
                    values(?, ?, ?)''', course_id, term.year, term.term)

        return course_id


