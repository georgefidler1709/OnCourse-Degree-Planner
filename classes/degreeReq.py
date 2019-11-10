"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degreeReq.py
Implementation of the DegreeReq class which specifies a degree requirement.
These requirements take the form of a count of units from a particular
filter of courses.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC, abstractmethod
from typing import List, Optional
from . import courseFilter
from . import program
from . import course
from . import degree
from . import api
# from . import minDegreeReq
from . import genEdFilter, freeElectiveFilter

class DegreeReq(ABC):

    def __init__(self, inFilter: Optional['courseFilter.CourseFilter'], uoc: int):
        # input as separate variables? or some other format
        self.uoc = uoc
        self.filter = inFilter
        super().__init__()

    def __repr__(self) -> str:
        return f"<DegreeReq uoc={self.uoc}, filter={self.filter}>"

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    # Note: Deletes matching courses from list!
    @abstractmethod
    def fulfilled(self, courses: List['course.Course'], degree: 'degree.Degree') -> bool:
        pass

    
    # Input: a degree and a list of courses
    # Return: number of units remaining to complete this requirement
    # Note: Deletes matching courses from list!
    @abstractmethod
    def remaining(self, courses: Optional[List['course.Course']],
            degree: Optional['degree.Degree']) -> int:
        pass

    # Return whether this filter is an overall requirement (e.g. must have completed 144 UoC total)
    def overall_requirement(self) -> bool:
        return self.filter is None

    # Return whether this is a core requirement
    def core_requirement(self) -> bool:
        if self.filter is None:
            return False
        return self.filter.core

    # Return whether this is a subject requirement
    def subj_requirement(self) -> bool:
        if (self.filter is not None and self.filter.field_filter):
            # WARNING not sure why subject requirements had to be min degree reqs before
            # and isinstance(self, minDegreeReq.MinDegreeReq)):
            return True
        else:
            return False

    # Return whether this is a gen ed requirement
    def gen_requirement(self) -> bool:
        if isinstance(self.filter, genEdFilter.GenEdFilter):
            return True
        else:
            return False

    # Return whether this is a free elective requirement
    def free_requirement(self) -> bool:
        if isinstance(self.filter, freeElectiveFilter.FreeElectiveFilter):
            return True
        else:
            return False

    # Saves the requirement in the database
    # Return: the id of the filter in the database
    def save(self):
        return self.filter.save()
