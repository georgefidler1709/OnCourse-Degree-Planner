"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

andFilter.py
A filter that only allows courses that match all of the provided filters

[MORE INFO ABOUT CLASS]
"""

from typing import List

import course
import courseFilter
import program


class AndFilter(courseFilter.CourseFilter):

    def __init__(self, filters: List[courseFilter.CourseFilter]):
        super().__init__()
        self.filters = filters

    # Returns whether this filters specific courses
    @property
    @abstractmethod
    def core(self) -> bool:
        for filter in self.filters:
            if not filter.core:
                return False
        return True

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: course.Course, program: program.Program) -> bool:
        # make an iterable where element at a position is True if the filter at that position accepts
        individual_acceptance = map(lambda x: x.accepts_course(course, program), self.filters)

        # Only accept if all of the filters accepted
        return all(individual_acceptance)
