import json;

"""
COMP4290 Group Project
Team: On course.Course
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
import courseEnrollment
import degreeReq

class Degree(object):

    def __init__(self, alpha_code: str, num_code: int, name: str, year: int, requirements:
            List['degreeReq.DegreeReq']):
        self.alpha_code = alpha_code
        self.num_code = num_code
        self.name = name
        self.year = year
        self.requirements = requirements

    # Input: either nothing or a list of completed courses (<List>CourseEnrollment)
    # Return: list of requirements remaining for completion
    def get_requirements(self, courses: List['courseEnrollment.CourseEnrollment']=None) -> List['degreeReq.DegreeReq']:
        # TODO
        pass

    # Input: list of courses completed
    # Return: boolean indicating whether degree completed
    def complete(self, courses: List['courseEnrollment.CourseEnrollment']) -> bool:
        # TODO
        # NOTE we might have to consider how to handle one course
        # fulfilling multiple requirements
        pass

    # Saves degree into the database
    # Return: the id of the degree
    def save(self) -> int:
        g.db.execute('insert or ignore into Degrees(name, code, id) values(?, ?, ?)', self.name,
                self.alpha_code,
                self.num_code)

        g.db.execute('insert into DegreeOfferings(year, degree_id) values (?, ?)', self.year,
                self.num_code)


        for requirement in self.requirements:
           filter_id = requirement.save()
           g.db.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
           offering_year_id, requirement_id, uoc_needed) values (?, ?, ?, ?)''', self.year,
           self.num_code, filter_id, requirement.uoc)

        return self.num_code


