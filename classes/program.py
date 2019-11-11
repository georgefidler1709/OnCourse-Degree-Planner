"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the Program class, which represents a specific program of
study.

[MORE INFO ABOUT CLASS]
"""

from typing import List, Optional, Dict

from . import course
from . import courseEnrollment
from . import degree
from . import degreeReq
from . import term
from . import api

from . import andFilter
from . import orFilter
from . import fieldFilter 
from . import freeElectiveFilter
from . import genEdFilter
from . import levelFilter
from . import specificCourseFilter


class Program(object):

    def __init__(self, degree: 'degree.Degree', courses_taken: List['courseEnrollment.CourseEnrollment'],
            prior_studies: List['course.Course']):
        self.degree = degree # degree.Degree
        self.courses = courses_taken # <List>CourseEnrollments
        self.prior_studies = prior_studies

    # Input: a course
    # Return: Whether there is already an enrollment for this course
    def enrolled(self, course: 'course.Course') -> bool:
        for c in self.prior_studies:
            if c == course:
                return True
        for enrollment in self.courses:
            if enrollment.course == course:
                return True
        return False

    # Input: a course
    # Return: term in which that course is taken
    def term_taken(self, course: 'course.Course') -> Optional['term.Term']:
        for enrollment in self.courses:
            if enrollment.course == course:
                return enrollment.term
        return None

    @property
    # Return: start year for program
    def intake_year(self) -> int:
        return self.degree.year

    @property
    # Return: final year for program
    def final_year(self) -> int:
        final = self.degree.year + self.degree.duration - 1
        for enrol in self.courses:
            if enrol.term.year > final:
                final = enrol.term.year
        return final

    def __repr__(self) -> str:
        return f"<Program degree={self.degree!r}, courses={self.courses!r}>"

    # Input: a course and a term of study
    # Create a course enrollment for that term and add to courses
    def add_course(self, course: 'course.Course', term: term.Term) -> None:
        if self.enrolled(course):
            return
        enrollment = courseEnrollment.CourseEnrollment(course, term)
        self.courses.append(enrollment)

    # Input: a course enrollment to remove
    # Remove enrollment from program
    def remove_course(self, course: 'courseEnrollment.CourseEnrollment') -> None:
        self.courses.remove(course)

    # Input: optionally, a term for which to count units
    # Return: how many units are currently taken in that term
    def unit_count_term(self, term: 'term.Term') -> int:
        units = 0
        for enrollment in self.courses:
            if enrollment.term == term:
                    units += enrollment.course.units
        return units

    # Input: optionally, a term up to which to count units
    # Return: how many units are currently taken up to that term, from the specified course list,
    # or if no term or courses specified, how many units in the program
    def unit_count_total(self, term: Optional['term.Term']=None,
                courses: Optional[List['course.Course']]=None) -> int:
        units = 0
        for c in self.prior_studies:
            if courses is None or c in courses:
                    units += c.units
        for enrollment in self.courses:
            if term is None or enrollment.term < term:
                if courses is None or enrollment.course in courses:
                    units += enrollment.course.units
        return units

    # Return: a list of the courses taken in this program
    def course_list(self) -> List['course.Course']:
        courses = []
        for c in self.prior_studies:
            courses.append(c)
        for enrollment in self.courses:
            courses.append(enrollment.course)
        return courses

    # Return: requirements remaining to complete the program
    def get_outstanding_reqs(self) -> Dict[('degreeReq.DegreeReq', int)]:
        return self.degree.get_requirements(self)

    def to_api(self) -> api.Program:
        # sort the enrolled courses by term then name
        enrollments_map: Dict[int, Dict[int, List[str]]]= {}
        for x in self.courses:
            enrollments_map.setdefault(x.term.year, {}).setdefault(x.term.term, []).append(x.course.course_code);

        enrollments: List["api.YearPlan"] = [ { 
                    "year": year, 
                    "term_plans": [ {
                        "term": term, 
                        "course_ids": courses,
                    } for (term, courses) in term_plan.items() ]
                } for (year, term_plan) in enrollments_map.items()];
            
        # TODO hardcode which reqs to output for now
        # until you fix the bug, then switch for commented out section below
        output_req_types = (fieldFilter.FieldFilter, 
            freeElectiveFilter.FreeElectiveFilter,
            levelFilter.LevelFilter,
            genEdFilter.GenEdFilter)
        outstanding_reqs = self.degree.requirements
        reqs: List['api.RemainReq'] = []
        for r in outstanding_reqs:
            if isinstance(r.filter, output_req_types):
                new: api.RemainReq = {'units': r.uoc, 'filter_type': r.filter.simple_name}
                reqs.append(new)

        # TODO this is the correct version, uncomment when
        # self.get_outstanding_reqs() is accurate
        '''
        outstanding_reqs = self.get_outstanding_reqs()

        reqs: List['api.RemainReq'] = []
        for key, val in outstanding_reqs.items():
            new: api.RemainReq = {'units': val, 'filter_type': key.filter.simple_name}
            reqs.append(new)                
        '''

        return {'id': self.degree.num_code, 
                'name': self.degree.name,
                'year': self.degree.year,
                'duration': self.degree.duration,
                'url': self.degree.get_url(),
                'reqs': reqs,
                'enrollments': enrollments};

    def get_generator_response_api(self) -> api.GeneratorResponse:
        return {'program': self.to_api(),
                'courses': {enrollment.course_code() : enrollment.course.to_api() for enrollment in self.courses}};
