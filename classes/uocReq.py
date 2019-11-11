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

    def __init__(self, uoc: int, filter: Optional['courseFilter.CourseFilter']):
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

    # Input: program.Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    def fulfilled(self, program: 'program.Program', term: 'term.Term',
            coreq: bool=False) -> bool:
        pass

    # Saves the requirement in the database
    # Return: the id of the requirement in the database
    def save(self) -> int:
        # TODO
        pass
