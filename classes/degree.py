"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degree.py
Implementation of the Degree class which is an object corresponding to a degree
offered by the university, and contains information about the degree completion
requirements.

[MORE INFO ABOUT CLASS]
"""

from flask import g
from typing import List

from degreeReq import DegreeReq

class Degree(object):

    def __init__(self, num_code: int, code: str, name: str, year: int, requirements: List[DegreeReq]):
        self.name = name
        self.num_code = num_code
        self.code = code
        self.year = year
        self.requirements = requirements
        # work out format of input
        # self.code = String
        # self.numCode = int
        # self.name = String
        # self.requirements = <List>DegreeReq

    # Input: either nothing or a list of completed courses (<List>CourseEnrollment)
    # Return: list of requirements remaining for completion
    def get_requirements(self, courses: list=None) -> list:
        # TODO
        pass

    # Input: list of courses completed
    # Return: boolean indicating whether degree completed
    def complete(self, courses: list) -> bool:
        # TODO
        # NOTE we might have to consider how to handle one course
        # fulfilling multiple requirements
        pass

    # Saves degree into the database
    # Return: the id of the degree
    def save(self) -> int:
        g.db.execute('insert or ignore into Degrees(name, code, id) values(?, ?, ?)', self.name, self.code,
                self.num_code)

        g.db.execute('insert into DegreeOfferings(year, degree_id) values (?, ?)', self.year,
                self.num_code)


        for requirement in self.requirements:
           filter_id = requirement.save() 
           g.db.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
           offering_year_id, requirement_id, uoc_needed) values (?, ?, ?, ?)''', self.year,
           self.num_code, filter_id, requirement.uoc)

        return self.num_code


