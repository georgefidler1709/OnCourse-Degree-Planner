"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

orReq.py
A course requirement that requires at least one of multiple requirements to be matched

[MORE INFO ABOUT CLASS]
"""

from typing import List

from . import compositeReq
from . import course
from . import courseReq
from . import term
from . import program


class OrReq(compositeReq.CompositeReq):

    def __init__(self, reqs: List['courseReq.CourseReq']):
        super().__init__(reqs)

    def __repr__(self) -> str:
        return f"<OrReq reqs={self.reqs!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        if top_level and exclusion:
            # For top level exclusions, we want to show it as a list
            return "\n".join(map(lambda x: x.info(), self.reqs))
        else:
            return "(" + " OR ".join(map(lambda x: x.info(), self.reqs)) + ")"

    @property
    def requirement_name(self) -> str:
        return "OrRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False) -> List[str]:
        errors = []
        if not self.fulfilled(program, term, coreq):
            errors.append(self.info())
        return errors


    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False) -> bool:
        individual_fulfills = map(lambda x: x.fulfilled(program, term, coreq),
                self.reqs)

        # Accept if any of the requirements are fulfilled
        return any(individual_fulfills)
    
    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
