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

    # Input: a core degree requirement
    # Append to a list of courses that fulfill this core requirement
    def fulfill_core_requirement(self, filter: 'courseFilter.CourseFilter',
                courses: List['course.Course']):

        if isinstance(filter, specificCourseFilter.SpecificCourseFilter):
            courses.append(filter.course)

        elif isinstance(filter, orFilter.OrFilter):
            self.fulfill_core_requirement(filter.filters[0], courses)

        elif isinstance(filter, andFilter.AndFilter):
            for f in filter.filters:
                self.fulfill_core_requirement(f, courses)

    # Input: a program of study and a course
    # Return: an appropriate term in which to take given course
    def find_term(self, prog: 'program.Program', course: 'course.Course') -> 'term.Term':
        for term in self.terms:
            # if we can take the course in this term
            if not course.has_offering(term):
                continue
            if prog.unit_count(term) + course.units <= self.term_unit_cap:
                if (course.prereqs_fulfilled(prog, term) and course.coreqs_fulfilled(prog, term)
                    and not course.excluded(prog, term)):
                    return term
        return None
    
    # Generate a program of study that fulfils the core units of the degree
    def generate(self) -> 'program.Program':
        # create program
        prog = program.Program(self.degree, [])
        courses = []

        # for each degree requirement, add courses to course list
        for req in self.degree.requirements:
            if not req.core_requirement:
                continue
            self.fulfill_core_requirement(req.filter, courses)

        # iterate for a max of n_courses times
        # to handle different orders of courses
        n_courses = len(courses)
        courseIter = courses.copy()
        for i in range(0, n_courses):

            # if all courses have been added
            if len(courses) == 0:
                break

            for c in courses:
                term = self.find_term(prog, c)
                if term is not None:
                    prog.add_course(c, term)
                    courseIter.remove(c)

            courses = courseIter.copy()

        # now assume all core requirements fulfilled
        return prog




