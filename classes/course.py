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

from flask import g
from typing import List

from courseReq import CourseReq
from program import Program

class Course(object):

    def __init__(self, code: str, name: str, units: int, terms: List[int],
            prereqs: CourseReq, coreqs: CourseReq, exclusions: CourseReq):
        # figure out inputs - database or variables?
        # to be assigned:
        self.code = code
        self.letter_code = code[:4]
        self.number_code = code[4:]
        self.level = int(self.number_code[0])
        self.name = name
        self.units = units
        # TODO: decide whether we want to allow different terms for different years
        self.years = [2020]
        self.terms = terms
        self.prereqs = prereqs
        self.coreqs = coreqs
        self.exclusions = exclusions

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
    def coreqsFulfilled(self, program: Program, term: int, additional_courses: List[Course]) -> bool:
        return self.coreqs.fulfilled(program, term, additional_courses, coreq=True)

    # THINK about corequisites - what if prerequisite OR corequisite?

    # Input: The program of the student trying to take the course, the term they are taking it in,
    # and any additional courses they are taking that term
    # Return: whether any exclusion courses have been taken
    def excluded(self, program: Program, term: int, additional_courses: List[Course]) -> bool:
        return self.exclusions.fulfilled(program, term, additional_courses, coreq=True)

    # Saves the course in the database
    # Return: the id of the course
    def save(self) -> int:
        prereq_id = self.prereqs.save()
        coreq_id = self.coreqs.save()
        exclusions_id = self.exclusions.save()

        # save the course itself
        g.db.execute('''insert into Courses(letter_code, number_code, level, name, units, prereq,
        coreq, exclusion) values (?, ?, ?, ?, ?, ?, ?)''',
        self.letter_code, self.number_code, self.level, self.name, self.units, prereq_id, coreq_id,
        exclusions_id)

        course_id = g.db.lastrowid

        # save the offerings of the course
        for year in self.years:
            for term in self.terms:
                g.db.execute('insert or ignore into Sessions(year, term) values(?, ?)', year, term)
                g.db.execute('''insert into CourseOfferings(course_id, session_year, session_term)
                        values(?, ?, ?)''', course_id, year, term)

        return course_id


