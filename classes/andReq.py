"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

andReq.py
A course requirement that requires multiple requirements to be matched

[MORE INFO ABOUT CLASS]
"""

from typing import List

from . import compositeReq
from . import course
from . import courseReq
from . import term
from . import program


class AndReq(compositeReq.CompositeReq):

    def __init__(self, reqs: List['courseReq.CourseReq']):
        super().__init__(reqs)

    def __repr__(self) -> str:
        return f"<AndReq reqs={self.reqs!r}>"
    
    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        if top_level and not exclusion:
            # For top level prereqs and coreqs, we want to show it as a list
            return "\n".join(map(lambda x: x.info(), self.reqs))
        else:
            return "(" + " AND ".join(map(lambda x: x.info(), self.reqs)) + ")"

    # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return "AndRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False, excl: bool=False) -> List[str]:
        errors: List[str] = []
        for req in self.reqs:
            errors = errors + req.check(program, term, coreq, excl)
        return errors

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass

