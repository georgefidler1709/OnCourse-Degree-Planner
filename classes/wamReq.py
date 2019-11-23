'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

wamReq.py
The course requirement to have a particular WAM
'''

from typing import List

from . import course
from . import degree
from . import term
from . import program
from . import singleReq

class WAMReq(singleReq.SingleReq):

    def __init__(self, wam: int):
        super().__init__()
        self.wam = wam

    def __repr__(self) -> str:
        return f'<WAMReq WAM>={self.wam!r}>'

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        return f'Required WAM of {self.wam!r} or more'

    @property
    def requirement_name(self) -> str:
        return 'WamRequirement'

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def check(self, program: program.Program, term: term.Term,
            coreq: bool=False, excl: bool=False) -> List[str]:
        errors = []
        errors.append(self.info())
        return errors


    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False, excl: bool=False) -> bool:
        return True
