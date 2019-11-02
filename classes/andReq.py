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

import compositeReq
import course
import courseReq
import term
import program


class AndReq(compositeReq.CompositeReq):

    def __init__(self, reqs: List[courseReq.CourseReq]):
        super().__init__(reqs)

    def __repr__(self) -> str:
        return f"<AndReq reqs={self.reqs!r}>"

    # The name of the requirement for the database
    @property
    def requirement_name(self) -> str:
        return "AndRequirement"

   # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: program.Program, term: term.Term,
            coreq: bool=False) -> bool:
        individual_fulfills = map(lambda x: x.fulfilled(program, term, coreq), self.reqs)

        # Only accept if all of the requirements accepted
        return all(individual_fulfills)

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass

