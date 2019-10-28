"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

generator.py
A generator which creates a degree plan for a given degree

[MORE INFO ABOUT CLASS]
"""
from typing import List
import program
import degree
import term
import specificCourseFilter
import orFilter
import andFilter

class Generator(object):

    def __init__(self, degree: 'degree.Degree'):
        self.degree = degree
        self.term_unit_cap = 18 # default for first release
        self.n_terms = 3 # 3 terms for first release
        self.terms = []
        # fill terms
        for year in range(degree.year, (degree.year + degree.duration)):
            for t in range(1, self.n_terms + 1):
                self.terms.append(term.Term(year, t))
        # TODO exclude terms
        # TODO add summer term
        # TODO term specific unit cap

    # Produce a list of courses that fulfill a core filter
    def handle_filter(self, filter: 'courseFilter.CourseFilter',
                courses: List['course.Course']):

        if isinstance(filter, specificCourseFilter.SpecificCourseFilter):
            courses.append(filter.course)

        elif isinstance(filter, orFilter.OrFilter):
            self.handle_filter(filter.filters[0], courses)

        elif isinstance(filter, andFilter.AndFilter):
            for f in filter.filters:
                self.handle_filter(f, courses)

    # given a core degree requirement, return a list of courses that would
    # fulfill that requirement
    def fulfill_core_requirement(self, req: 'degreeReq.DegreeReq') -> List['course.Course']:
        courses = []
        self.handle_filter(req.filter, courses)
        # assert req.fulfilled(courses)
        return courses

    # find an appropriate term in which to take a given course
    def find_term(self, prog: 'program.Program', course: 'course.Course') -> 'term.Term':
        for term in self.terms:
            # if we can take the course in this term
            if prog.unit_count(term) <= self.term_unit_cap + course.units:
                if course.has_offering(term) and course.prereqs_fulfilled(prog, term):
                    # what about coreqs? exclusions?
                    return term
        return None
    
    # Generate a program of study that fulfils the core units of the degree
    def generate(self) -> 'program.Program':
        # create program
        prog = program.Program(self.degree, [])

        # for each degree requirement, attempt to fulfill
        # handle only core requirements
        for req in self.degree.requirements:
            if req.core_requirement:
                courses = self.fulfill_core_requirement(req)
                for course in courses:
                    term = self.find_term(prog, course)
                    prog.add_course(course, term)

        # now assume all core requirements fulfilled
        return prog




