'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

program.py
Implementation of the Program class, which represents a specific program of
study.
'''

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
    # Return: final calendar year for program
    def final_year(self) -> int:
        final = self.degree.year + self.degree.duration - 1
        for enrol in self.courses:
            if enrol.term.year > final:
                final = enrol.term.year
        return final

    def matching_year(self, term: 'term.Term', year: int) -> bool:
        if year >= 0:
            # 8 courses per year full time load = 48 uoc
            if self.unit_count_total(term) >= (year-1)*48:
                return True
            if term.year >= self.intake_year + year - 1:
                return True
        else:
            if self.unit_count_total(term) >= (self.degree.duration + year)*48:
                return True
            if term.year >= self.final_year + year + 1:
                return True
        return False


    def __repr__(self) -> str:
        return f'<Program degree={self.degree!r}, courses={self.courses!r}>'

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
    # is a dict of degreerequirement and corresponding number of UOC needed
    def get_outstanding_reqs(self) -> Dict[('degreeReq.DegreeReq', int)]:
        return self.degree.get_requirements(self)

    # Return: a list of tuples containing a course code and a list of errors
    # pertaining to the requirements of that course
    def check_course_reqs(self) -> Dict[str, List[api.CourseReq]]:
        errors = {}
        for enrol in self.courses:
            course_errors = enrol.course.check_reqs(self, enrol.term)
            if len(course_errors) > 0:
                errors[enrol.course.course_code] = course_errors;
        return errors

    def check_course_warnings(self) -> Dict[str, List[str]]:
        errors = {}
        for enrol in self.courses:
            course_errors = enrol.course.check_warnings(self, enrol.term)
            if len(course_errors) > 0:
                errors[enrol.course.course_code] = course_errors
        return errors

    def get_reqs_api(self) -> List['api.RemainReq']:
        outstanding_reqs = self.get_outstanding_reqs()

        reqs: List['api.RemainReq'] = []
        for key, val in outstanding_reqs.items():

            new: api.RemainReq = {'units': val, 'filter_type': '', 'info': ''}
            if key.alttext:
                new = {'units': val,
                    'filter_type': 'Special requirement',
                    'info': key.alttext,
                }
            elif key.filter:
                new = {'units': val,
                    'filter_type': key.filter.simple_name,
                    'info': key.filter.info
                }

            reqs.append(new)
        return reqs;


    def to_api(self) -> api.Program:
        # sort the enrolled courses by term then name
        enrollments_map: Dict[int, Dict[int, List[str]]]= {}

        # initialize an empty enrollments map from start year to end year
        # puts default values for all years and all terms (WARNING no summer term)
        if len(self.courses) > 0:
            start_year = min(self.courses, key=lambda x: x.term.year).term.year
            end_year = max(self.courses, key=lambda x: x.term.year).term.year
        else:
            start_year = self.degree.year
            end_year = start_year + (self.degree.duration - 1)

        for year in range(start_year, end_year + 1):
            term_dict: Dict[int, List[str]] = {}
            for term in range(1, 3 + 1):
                term_dict[term] = []
            enrollments_map[year] = term_dict

        # fill in data from course enrollments
        for x in self.courses:
            enrollments_map[x.term.year][x.term.term].append(x.course.course_code)

        enrollments: List['api.YearPlan'] = [ { 
                    'year': year,
                    'term_plans': [ {
                        'term': term,
                        'course_ids': courses,
                    } for (term, courses) in term_plan.items() ]
                } for (year, term_plan) in enrollments_map.items()];

        return {'id': self.degree.num_code,
                'name': self.degree.name,
                'year': self.degree.year,
                'duration': self.degree.duration,
                'url': self.degree.get_url(),
                'notes': self.degree.notes, # TODO add this to front end
                'enrollments': enrollments,
                'done': []}

    def get_prereq_conflicts_api(self) -> api.CheckResponse:
        return {'degree_reqs': self.get_reqs_api(),
                'course_reqs': self.check_course_reqs(),
                'course_warn': self.check_course_warnings() };

    def get_generator_response_api(self) -> api.GeneratorResponse:
        full_reqs = Program(self.degree, [], []).get_reqs_api()

        return {'program': self.to_api(),
                'courses': {enrollment.course_code() : enrollment.course.to_api() for enrollment in self.courses},
                'reqs': self.get_prereq_conflicts_api(),
                'full_reqs': full_reqs };

