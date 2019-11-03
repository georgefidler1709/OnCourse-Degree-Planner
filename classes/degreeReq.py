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

from . import andFilter
from . import orFilter
from . import fieldFilter 
from . import freeElectiveFilter
from . import genEdFilter
from . import levelFilter
from . import specificCourseFilter



class DegreeReq(ABC):

    def __init__(self, inFilter: 'courseFilter.CourseFilter', uoc: int):
        # input as separate variables? or some other format
        self.uoc = uoc
        self.filter = inFilter
        super().__init__()

    def __repr__(self) -> str:
        return f"<DegreeReq uoc={self.uoc}, filter={self.filter}>"

    # Input: a degree and a list of courses
    # Return: whether this course list would fulfil this degree requirement
    @abstractmethod
    def fulfilled(self, courses: List['course.Course'], deg: 'degree.Degree') -> bool:
        pass

    # Return whether this is a core requirement
    def core_requirement(self) -> bool:
        return self.filter.core

    # Saves the requirement in the database
    # Return: the id of the filter in the database
    def save(self):
        return self.filter.save()

    # returns a string representing the type of DegreeReq
    def type_to_str(self) -> str:
        if isinstance(self, andFilter.AndFilter):
            filter_type = "and"
        elif isinstance(self, orFilter.OrFilter):
            filter_type = "or"
        elif isinstance(self, fieldFilter.FieldFilter):
            filter_type = "field"
        elif isinstance(self, freeElectiveFilter.FreeElectiveFilter):
            filter_type = "free elective"
        elif isinstance(self, genEdFilter.GenEdFilter):
            filter_type = "general education"
        elif isinstance(self, levelFilter.LevelFilter):
            filter_type = "level"
        elif isinstance(self, specificCourseFilter.SpecificCourseFilter):
            filter_type = "specific course"
        else:
            filter_type = "mystery"

        return filter_type


    # TODO want to make a to_api() function to have UOC counts for type of filter
    # but will have to make those changes for self.filter as well
    # outputs counts 
    # def to_api(self) -> api.DegreeReq:
    #     # convert the filter type to a string
    #     # doesn't work nicely for AND and OR requirements,
    #     # but the API doesn't want specific course ones so should be ok

    #     if isinstance(self, andFilter.AndFilter):
    #         filter_type = "and"
    #     elif isinstance(self, orFilter.OrFilter):
    #         filter_type = "or"
    #     elif isinstance(self, fieldFilter.FieldFilter):
    #         filter_type = "field"
    #     elif isinstance(self, freeElectiveFilter.FreeElectiveFilter):
    #         filter_type = "free elective"
    #     elif isinstance(self, genEdFilter.GenEdFilter):
    #         filter_type = "general education"
    #     elif isinstance(self, specificCourseFilter.SpecificCourseFilter):
    #         filter_type = "specific course"
    #     else:
    #         filter_type = "mystery"

    #     return {'units': units,
    #             'filter_type': filter_type}

