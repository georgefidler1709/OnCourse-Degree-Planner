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

from typing import List, Optional, Dict, Tuple

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
        for enrollment in self.courses:
            if term is None or enrollment.term < term:
                if courses is None or enrollment.course in courses:
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

    # Return: a list of tuples containing a course code and a list of errors
    # pertaining to the requirements of that course
    def check_course_reqs(self) -> List[Tuple[str, List[Tuple[str, List[str]]]]]:
        errors = []
        for enrol in self.courses:
            course_errors = enrol.course.check_reqs(self, enrol.term)
            if len(course_errors) > 0:
                errors.append((enrol.course.course_code, course_errors))
        return errors

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
                new = {'units': val, 
                    'filter_type': key.filter.simple_name,
                    'info': key.filter.info
                }

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
