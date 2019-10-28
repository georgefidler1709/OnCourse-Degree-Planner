"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

generator.py
A generator which creates a degree plan for a given degree

[MORE INFO ABOUT CLASS]
"""

import program
import degree
import term

class Generator(object):

    def __init__(self, degree: 'degree.Degree'):
        self.degree = degree
        self.term_unit_cap = 18 # default for first release
        self.n_terms = 3 # 3 terms for first release
        self.terms = []
        # fill terms
        for year from degree.year to (degree.year + degree.duration - 1):
            for term from 1 to self.n_terms:
                self.terms.append(Term(year, term))
        # TODO exclude terms
        # TODO add summer term
        # TODO term specific unit cap

    # Generate a program of study that fulfils the core units of the degree
    def generate(self) -> 'program.Program':
        # create program
        self.program = program.Program(self.degree, [])

        # for each degree requirement, attempt to fulfill
        # handle only core requirements
        for req in degree.requirements:
            if req.core_requirement:
                courses = fulfill_core_requirement(req)
                for course in courses:
                    term = find_term(course)
                    self.program.add_course(course, term)

        # now assume all core requirements fulfilled
        return program

    # given a core degree requirement, return a list of courses that would
    # fulfill that requirement
    def fulfill_core_requirement(self, req: 'degreeReq.DegreeReq') -> List['course.Course']:
        courses = handle_filter(req.filter, [])
        # assert req.fulfilled(courses)
        return courses

    # find an appropriate term in which to take a given course
    def find_term(self, course: 'course.Course') -> 'term.Term':
        for term in self.terms:
            # if we can take the course in this term
            if program.unit_count(term) <= self.unit_cap_term + course.units:
                if course.has_offering(term) and course.prereqs_fulfilled(program, term):
                    # what about coreqs? exclusions?
                return term
        return None
    
    # Produce a list of courses that fulfill a core filter
    def handle_filter(self, filter: 'courseFilter.CourseFilter',
                courses: List['course.Course']) -> List['course.Course']:

        if isinstance(filter, SpecificCourseFilter):
            courses.append(filter.course)

        else if isinstance(filter, OrFilter):
            handle_filter(filter.filters[0], courses)

        else if isinstance(filter, AndFilter):
            for f in filter.filters:
                handle_filter(f, courses)

        return courses






