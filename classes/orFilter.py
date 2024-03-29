'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

orFilter.py
A filter that allows courses that match any of the provided filters
'''

from typing import List

from . import course
from . import courseFilter
from . import degree


class OrFilter(courseFilter.CourseFilter):

    def __init__(self, filters: List['courseFilter.CourseFilter']):
        super().__init__()
        self.filters = filters

    # Returns whether this filters specific courses
    @property
    def core(self) -> bool:
        return all(map(lambda x: x.core, self.filters))

    @property
    def field_filter(self) -> bool:
        return any(map(lambda x: x.field_filter, self.filters))

    def __repr__(self) -> str:
        return f'<OrFilter filters={self.filters!r}>'

    # The name of the requirement for the database
    @property
    def filter_name(self) -> str:
        return 'OrFilter'

    # simple name for an Or is for front-end purposes
    # so get the name of one of its components
    @property
    def simple_name(self) -> str:
        # if len(self.filters) != 0:
        #     return self.filters[0].simple_name
        # else:
        #     return 'Or'

        # return 'Choose from these requirements'

        return 'Courses with options'

    @property
    def info(self) -> str:
        res = ''
        for f in self.filters:
            if res != '':
                res += ' OR '
            # res += f.info
            res += '(' + f.info + ')'

        return res

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        # make an iterable where element at a position is True if the filter at that position accepts
        individual_acceptance = map(lambda x: x.accepts_course(course, degree, eq), self.filters)

        # accept if any of the filters accepts
        return any(individual_acceptance)
