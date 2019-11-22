'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

unparsedReq.py
A course requirement that has not properly been parsed by the parser

'''

from typing import List

from . import course
from . import degree
from . import term
from . import program
from . import singleReq

class UnparsedReq(singleReq.SingleReq):

    def __init__(self, requirement_string: str):
        super().__init__()

        self.requirement_string = requirement_string

    def __repr__(self) -> str:
        return f'<UnparsedReq requirement_string={self.requirement_string!r}>'

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        return f'Requirements that we aren\'t checking: \'{self.requirement_string}\''

    # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return 'UnparsedRequirement'

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
                coreq: bool=False) -> List[str]:
        return []

    # Return: all necessary warnings for this course regarding min marks required for enrollment
    def mark_warnings(self, program: 'program.Program', term: 'term.Term') -> List[str]:
        return [f'Check if you meet the requirements: \'{self.requirement_string}\'']


