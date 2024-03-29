'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

generator.py
A generator which creates a degree plan for a given degree
'''

from typing import List, Optional
from . import program
from . import degree
from . import university
from . import term
from . import specificCourseFilter
from . import orFilter
from . import andFilter
from . import courseFilter
from . import course
from . import degreeReq

class Generator(object):

    def __init__(self, degree: 'degree.Degree', university: 'university.University',
            prior_studies: Optional[List['course.Course']]=None):
        self.university = university
        self.degree = degree
        self.term_unit_cap = 18 # default for first release
        self.n_terms = 3 # 3 terms for first release
        self.terms: List[term.Term] = []
        # fill terms
        for year in range(degree.year, (degree.year + degree.duration)):
            for t in range(1, self.n_terms + 1):
                self.terms.append(term.Term(year, t))
        if prior_studies:
            self.prior_studies = prior_studies
        else:
            self.prior_studies = []
        # TODO exclude terms
        # TODO add summer term
        # TODO term specific unit cap

    # Input: a core degree requirement
    # Append to a list of courses that fulfill this core requirement
    def fulfill_core_requirement(self, prog: 'program.Program', req: 'degreeReq.DegreeReq',
                courses: List['course.Course']) -> None:
        assert req.core_requirement()
        # mypy doesn't realise that core requires filter to not be None, so make an explicit check
        assert req.filter is not None
        # assert isinstance(self.university, university.University)
        course_options: List['course.Course'] = self.university.filter_courses(req.filter,
                prog.degree, eq=False)
        units: int = 0
        fulfilled: bool = False
        for c in course_options:
            if units >= req.uoc:
                break
            # handle prior studies
            for prior in self.prior_studies:
                if c == prior or c.equivalent(prior):
                    fulfilled = True
                    units += prior.units
            if fulfilled:
                fulfilled = False
                continue
            courses.append(c)
            units += c.units

    # Input: a program of study and a course
    # Return: an appropriate term in which to take given course
    def find_term(self, prog: 'program.Program', course: 'course.Course') -> Optional['term.Term']:
        for term in self.terms:
            # if we can take the course in this term
            if not course.has_offering(term):
                continue
            if prog.unit_count_term(term) + course.units <= self.term_unit_cap:
                if (course.prereqs_fulfilled(prog, term) and course.coreqs_fulfilled(prog, term)
                    and not course.excluded(prog, term)):
                    return term
        return None

    # Generate a program of study that fulfils the core units of the degree
    def generate(self) -> 'program.Program':
        # create program
        prog = program.Program(self.degree, [], self.prior_studies)
        courses: List['course.Course'] = []

        # for each degree requirement, add courses to course list
        for req in self.degree.requirements:
            if req.core_requirement():
                self.fulfill_core_requirement(prog, req, courses)

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

            for c in courses:
                if c.equivalents is None:
                    continue
                for e in c.equivalents:
                    equivalent = self.university.find_course(e)
                    if equivalent is not None:
                        term = self.find_term(prog, equivalent)
                        if term is not None:
                            prog.add_course(equivalent, term)
                            courseIter.remove(c)
                            break

            courses = courseIter.copy()


        # now assume all core requirements fulfilled
        return prog




