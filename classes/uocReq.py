"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

uocReq.py
The course requirement to have completed a certain number of units of credit prior
to enrolling, sometimes from a specific list of subjects

[MORE INFO ABOUT CLASS]
"""

from typing import List, Optional

from . import course
from . import courseFilter
from . import term
from . import program
from . import singleReq


class UOCReq(singleReq.SingleReq):

    def __init__(self, uoc: int, filter: Optional['courseFilter.CourseFilter']=None):
        super().__init__()
        self.uoc = uoc
        self.filter = filter

    def __repr__(self) -> str:
        return f"<UOCReq uoc={self.uoc!r}, filter={self.filter!r}>"

    def info(self, top_level: bool=False, exclusion: bool=False) -> str:
        if self.filter is None:
            return f"{self.uoc} UoC"
        else:
            return f"{self.uoc} UoC fulfilling [{self.filter.info()}]"

    @property
    def requirement_name(self) -> str:
        return "UocRequirement"

    # Input: a program and a term in which the required course is taken
    # Return: any errors pertaining to this requirement
    def check(self, program: 'program.Program', term: 'term.Term',
        coreq: bool=False, excl: bool=False) -> List[str]:
        errors = []
        if self.filter is None:
            if program.unit_count_total(term) < self.uoc:
                errors.append(self.info())
            return errors

        units = 0
        courses = program.course_list()
        for c in courses:
            if self.filter.accepts_course(c, program.degree):
                if (coreq and program.term_taken(c) <= term) or (program.term_taken(c) < term):
                    units += c.units
        if units < self.uoc:
            errors.append(self.info())
        return errors

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
