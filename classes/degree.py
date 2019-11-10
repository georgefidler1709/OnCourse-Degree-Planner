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
            faculty: str, requirements: Sequence['degreeReq.DegreeReq'], alpha_code: str):
        self.num_code = num_code
        self.alpha_code = alpha_code
        self.name = name
        self.year = year
        self.duration = duration
        self.faculty = faculty
        self.requirements = requirements

    def __repr__(self) -> str:
        return f"<Degree num_code={self.num_code!r}, name={self.name!r}, year={self.year!r}, duration={self.duration!r}, requirements={self.requirements!r}>"

    # Input: either nothing or a list of completed courses (<List>CourseEnrollment)
    # Return: list of requirements remaining for completion

    def get_requirements(self, program: Optional['program.Program']=None) -> Dict[('degreeReq.DegreeReq', int)]:
        remaining = {}
        # if there isn't a program, pass in None's to DegreeRequirement.remaining()
        courses: Optional[List['course.Course']] = None
        degree: Optional['Degree'] = None
        if program:
            courses = program.course_list()
            degree = program.degree
            
            

        # split the requirements into types
        core_reqs = [ x for x in self.requirements if x.core_requirement() ]
        subj_reqs = [ x for x in self.requirements if x.subj_requirement() ]
        gen_reqs = [ x for x in self.requirements if x.gen_requirement() ]
        free_reqs = [ x for x in self.requirements if x.free_requirement() ]

        # core requirement
        for req in core_reqs:
            # requirement is outstanding if you don't have a Program (no enrollments)
            # or if your current Program doesn't fulfill this requirement
            if not program or not (courses and degree and req.fulfilled(courses, degree)):
                # print(f"-----> core requirement {req}")
                remaining[req] = req.remaining(courses, degree)
        
        # subject req
        for req in subj_reqs:
            if not program or not (courses and degree and req.fulfilled(courses, degree)):
                # print(f"-----> subject requirement {req}")
                remaining[req] = req.remaining(courses, degree)

        # gen ed
        for req in gen_reqs:
            if not program or not (courses and degree and req.fulfilled(courses, degree)):
                # print(f"-----> gen ed requirement {req}")
                remaining[req] = req.remaining(courses, degree)

        # free elec
        for req in free_reqs:
            if not program or not (courses and degree and req.fulfilled(courses, degree)):
                # print(f"-----> free elec requirement {req}")
                remaining[req] = req.remaining(courses, degree)

        return remaining

    # Input: list of courses completed
    # Return: boolean indicating whether degree completed
    # NOTE we might have to consider how to handle one course
    # fulfilling multiple requirements
    def complete(self, program: 'program.Program') -> bool:
        remaining = self.get_requirements()
        if len(remaining) == 0:
            return True
        return False

    # Returns the handbook URL for this degree
    # depend on `self.num_code` and `self.year`
    def get_url(self) -> str:
        # for extensibility to postgraduate
        study_level = "undergraduate"
        url = f"https://www.handbook.unsw.edu.au/{study_level}/programs/{self.year}/{self.num_code}"
        return url

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
