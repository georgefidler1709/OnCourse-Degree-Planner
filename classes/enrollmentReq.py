'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

enrollmentReq.py
The course requirement to be enrolled in a specific degree program
'''

from typing import List

from . import course
from . import degree
from . import term
from . import program
from . import singleReq

class EnrollmentReq(singleReq.SingleReq):

    def __init__(self, degree_id: str, degree_name: str):
        super().__init__()
        self.degree_id = degree_id
        self.degree_name = degree_name

    def __repr__(self) -> str:
        return f'<EnrollmentReq degree_id={self.degree_id!r}, degree_name={self.degree_name!r}>'

    def info(self, top_leve: bool=False, exclusion: bool=False) -> str:
        return f'Enrollment in {self.degree_name} ({self.degree_id})'

    @property
    def requirement_name(self) -> str:
        return 'CurrentDegreeRequirement'

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False) -> List[str]:
        if program.degree.num_code != self.degree_id:
            return[self.info()]
        else:
            return []
