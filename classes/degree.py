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
from typing import Dict, Optional, Sequence, List

from . import courseEnrollment, course
from . import degreeReq
from . import program
from . import genEdFilter
from . import freeElectiveFilter
from . import minDegreeReq

class Degree(object):

    def __init__(self, num_code: int, name: str, year: int, duration: int, 
            faculty: str, requirements: Sequence['degreeReq.DegreeReq'], alpha_code: str,
            notes: List[str]=[]):
        self.num_code = num_code
        self.alpha_code = alpha_code
        self.name = name
        self.year = year
        self.duration = duration
        self.faculty = faculty
        self.requirements = requirements
        self.notes = notes

    def __repr__(self) -> str:
        return f"<Degree num_code={self.num_code!r}, name={self.name!r}, year={self.year!r}, duration={self.duration!r}, requirements={self.requirements!r}>"

    # Input: either nothing or a list of completed courses (<List>CourseEnrollment)
    # Return: list of requirements remaining for completion

    def get_requirements(self, program: Optional['program.Program']=None) -> Dict[('degreeReq.DegreeReq', int)]:
        remaining = {}
        # if there isn't a program, pass in None's to DegreeRequirement.remaining()
        courses: List['course.Course'] = []
        if program:
            courses = program.course_list()
            
        # split the requirements into types
        core_reqs = [ x for x in self.requirements if x.core_requirement() ]
        subj_reqs = [ x for x in self.requirements if x.subj_requirement() ]
        gen_reqs = [ x for x in self.requirements if x.gen_requirement() ]
        free_reqs = [ x for x in self.requirements if x.free_requirement() ]

        reqs = core_reqs + subj_reqs + gen_reqs + free_reqs
        for req in reqs:
            # requirement is outstanding if you don't have a Program (no enrollments)
            # or if your current Program doesn't fulfill this requirement
            rem, matched = req.remaining(courses, self)
            if not req.fulfilled(courses, self):
                remaining[req] = rem
            for c in matched:
                courses.remove(c)

        return remaining

    # Input: list of courses completed
    # Return: boolean indicating whether degree completed
    # NOTE we might have to consider how to handle one course
    # fulfilling multiple requirements
    def complete(self, program: 'program.Program') -> bool:
        remaining = self.get_requirements(program)
        if not remaining:
            return True
        return False

    # Returns the handbook URL for this degree
    # depend on `self.num_code` and `self.year`
    def get_url(self) -> str:
        # for extensibility to postgraduate
        study_level = "undergraduate"
        url = f"https://www.handbook.unsw.edu.au/{study_level}/programs/{self.year}/{self.num_code}"
        return url

    # Defines what it means for two degrees to be equal
    def __eq__(self, other) -> bool:
        if not isinstance(other, Degree):
            return False
        if int(self.num_code) ==  int(other.num_code):
            if self.year == other.year:
                return True
        return False

    # Saves degree into the database
    # Return: the id of the degree
    def save(self) -> int:
        g.db.execute('insert or ignore into Degrees(name, code, id) values(?, ?, ?)', self.name,
                self.name,
                self.num_code)

        g.db.execute('insert into DegreeOfferings(year, degree_id) values (?, ?)', self.year,
                self.num_code)


        for requirement in self.requirements:
           filter_id = requirement.save()
           g.db.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
           offering_year_id, requirement_id, uoc_needed) values (?, ?, ?, ?)''', self.year,
           self.num_code, filter_id, requirement.uoc)

        return self.num_code
