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

    def __init__(self, degree: 'degree.Degree', coursesTaken: List['courseEnrollment.CourseEnrollment']):
        self.degree = degree # degree.Degree
        self.courses = coursesTaken # <List>CourseEnrollments

        # for debugging
        # rem = degree.get_requirements(self)
        # for r in rem:
        #     print(r.filter.filter_name, rem[r])
        #     if isinstance(r.filter, andFilter.AndFilter) or isinstance(r.filter, orFilter.OrFilter):
        #         for f in r.filter.filters:
        #             if isinstance(f, specificCourseFilter.SpecificCourseFilter):
        #                 print(f.course.course_code)
            

    # Input: a course
    # Return: Whether there is already an enrollment for this course in this term
    def enrolled(self, course: 'course.Course') -> bool:
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
    # Return: how many units are currently taken in that term, or if no term specified,
    # how many units in the program
    def unit_count(self, term: Optional['term.Term']=None) -> int:
        units = 0
        for enrollment in self.courses:
            if enrollment.term == term or term is None:
                units += enrollment.course.units
        return units

    # Return: a list of the courses taken in this program
    def course_list(self) -> List['course.Course']:
        courses = []
        for enrollment in self.courses:
            courses.append(enrollment.course)
        return courses

    # Return: requirements remaining to complete the program
    # is a dict of degreerequirement and corresponding number of UOC needed
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
        
        outstanding_reqs = self.get_outstanding_reqs()

        reqs: List['api.RemainReq'] = []
        for key, val in outstanding_reqs.items():

            new: api.RemainReq = {'units': val, 'filter_type': '', 'info': ''}
            if key.filter:
                new = {'units': val, 'filter_type': key.filter.simple_name,
                    'info': key.filter.info}

            reqs.append(new)                
        

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
