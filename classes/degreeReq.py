'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degreeReq.py
Implementation of the DegreeReq class which specifies a degree requirement.
These requirements take the form of a count of units from a particular
filter of courses.
'''

from abc import ABC, abstractmethod
from typing import List, Optional, Tuple
from . import courseFilter
from . import program
from . import course
from . import degree
from . import api
from . import genEdFilter, freeElectiveFilter

class DegreeReq(ABC):

    def __init__(self, inFilter: Optional['courseFilter.CourseFilter'], uoc: int, alttext: Optional[str]=None):
        # input as separate variables? or some other format
        self.uoc = uoc
        self.filter = inFilter
        self.alttext = alttext
        super().__init__()

    def __repr__(self) -> str:
        return f'<DegreeReq uoc={self.uoc}, filter={self.filter}, alttext={self.alttext}>'

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
            degree: Optional['degree.Degree']) -> Tuple[int, List['course.Course']]:
        pass

    # Return whether this filter is an overall requirement (e.g. must have completed 144 UoC total)
    def overall_requirement(self) -> bool:
        return self.filter is None

    # the conditions for these checking functions
    # help to establish a hierarchy of requirements

    # Return whether this is a core requirement
    def core_requirement(self) -> bool:
        if self.filter is None:
            return False
        return self.filter.core

    # Return whether this is a subject requirement
    def subj_requirement(self) -> bool:
        from . import minDegreeReq

        if (self.filter is not None and self.filter.field_filter
            and isinstance(self, minDegreeReq.MinDegreeReq)):
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
