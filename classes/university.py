"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

university.py
Implementation of the University class which is a database of courses and programs

[MORE INFO ABOUT CLASS]
"""

from typing import Dict, List, Optional, Tuple
from flask import g

import degree
import degreeReq
import course
import courseReq
import courseFilter
import term

# Temporary: only allow 2019 results
YEAR = 2019


class University(object):

    def __init__(self, degrees: List['degree.Degree'], courses: List['course.Course']):
        # need to decide how degree/course details passed in
        # unpack and create degree.Degree and course.Course objects
        self.degrees = degrees
        self.courses = courses
        self.course_requirement_types = self.load_course_requirement_types()
        self.course_filter_types = self.load_course_filter_types()

    # Input: degree letter code (eg. COMPA1)
    # Return: corresponding degree.Degree object
    def findDegreeByLetterCode(self, letter_code: str) -> Optional['degree.Degree']:
        response = g.query_db('''select id
                                 from Degrees
                                 where code = ?''', (letter_code,), one=True)
        if response is None:
            # No degree with that code, so return nothing
            return None
        else:
            numeric_code = response[0]
            return self.findDegreeByNumberCode(numeric_code)

    # Input: degree numerical code (eg. 3778)
    # Return: corresponding Degree object
    def findDegreeByNumberCode(self, numeric_code: int) -> Optional['degree.Degree']:
        return self.load_degree(numeric_code, need_requirements = True)

    # Input: degree numerical code (eg. 3778), whether we need the requirements for the degree
    # (eg. if we're just loading the degree as part of a course requirement we don't need the
    # requirements)
    # Return: corresponding Degree object
    def load_degree(self, numeric_code: int, need_requirements: bool=True) -> Optional['degree.Degree']:
        year = YEAR
        response = g.query_db('''select name, code
                                 from Degrees
                                 where id = ?''', (numeric_code,), one=True)

        if response is None:
            # No degree with that code, so return nothing
            return None
            
        name, alpha_code = response

        # Get all of the requirements for the degree
        response = g.query_db('''select uoc_needed, requirement_id
                                 from DegreeOfferingRequirements
                                 where offering_degree_id = ?
                                 and offering_year_id = ?''')

        requirements = []

        if need_requirements:
            for offering_requirement in response:
                uoc, filter_id = offering_requirement
                filter = self.load_course_filter(filter_id)
                
                if filter_id is not None:
                    requirement = degreeReq.DegreeReq(filter, uoc)
                    requirements.append(requirement)
                else:
                    # Filter should not be None
                    print("ERROR: filter {} for degree requirement should not be null".format(filter_id))

        return degree.Degree(alpha_code, numeric_code, name, year, requirements)

    # Input: course code (eg. COMP1511)
    # Return: corresponding Course object from courses
    def findCourse(self, code: str) -> Optional['course.Course']:
        subject = code[:4]
        numeric_code = int(code[4:])
        return self.load_course(subject, numeric_code, need_requirements=True)

    # Input: course subject (eg. COMP), numeric code (eg. 1511) and whether we need the requirements
    # (same as for load_degree)
    # Return: corresponding Course object
    def load_course(self, subject: str, numeric_code: int, need_requirements: bool=True) -> Optional['course.Course']: 
        response = g.query_db('''select id, name, units, prereq, coreq, exclusion
                                 from Courses
                                 where letter_code = ?
                                 and number_code = ?''', subject, str(numeric_code), one=True)

        if response is None:
            # No matching course
            return None

        course_id, name, units, prereq_id, coreq_id, exclusion_id = response

        # Get the terms that the course runs in
        response = g.query_db('''select session_year, session_term
                                 from CourseOfferings
                                 where course_id = ?''', course_id)
        terms = []
        for year, term_num in response:
            terms.append(term.Term(year, term_num))

        if need_requirements:
            prereq = load_course_requirement(prereq_id)
            coreq = load_course_requirement(coreq_id)
            exclusion = load_course_requirement(exclusion_id)
        else:
            prereq = None
            coreq = None
            exclusion = None

        return course.Course(subject, numeric_code, name, units, terms, prereq, coreq, exclusion)

    # Input: A filter string [ITEMISE THESE HERE]
    # Return: List of courses that match the requested filter
    def filterCourses(self, filter: 'courseFilter.CourseFilter') -> List['course.Course']:
        # TODO
        pass

    # Return: A dictionary containing the ids of each course requirement type along with their names
    def load_course_requirement_types(self) -> Dict[int, str]:
        requirement_types: Dict[int, str] = {}
        response = g.query_db('''select id, name
                                 from CourseRequirementTypes''')

        for requirement_type in response:
            type_id, type_name = requirement_type
            requirement_types[type_id] = type_name

        return requirement_types

    # Return: A dictionary containing the ids of each course filter type along with their names
    def load_course_filter_types(self) -> Dict[int, str]:
        filter_types: Dict[int, str] = {}
        response = g.query_db('''select id, name
                                 from CourseFilterTypes''')

        for filter_type in response:
            type_id, type_name = filter_type
            filter_types[type_id] = type_name

        return filter_types

    # Input: the id of the course requirement
    # Return: The course requirement in question
    def load_course_requirement(self, requirement_id: int) -> Optional['courseReq.CourseReq']:
        response = g.query_db('''select *
                                 from CourseRequirements
                                 where id = ?''', requirement_id, one=True)

        if response is None:
            # Failed to load course requirement
            print("ERROR: No course requirement {}".format(requirement_id))
            return None
        
        requirement_data = response
        type_id = requirement_data['type_id']
        type_name = self.course_requirement_types.get(type_id, None)
        if type_name is None:
            # Invalid course requirement type
            print("ERROR: invalid course requirement type {}".format(type_id))
            return None

        # Determine which course type it is from the name
        if type_name == 'CompletedCourseRequirement':
            return load_completed_course_requirement(requirement_data)
        elif type_name == 'CurrentDegreeRequirement':
            return load_current_degree_requirement(requirement_data)
        elif type_name == 'YearRequirement':
            return load_year_requirement(requirement_data)
        elif type_name == 'UocRequirement':
            return load_uoc_requirement(requirement_data)
        elif type_name == 'and_requirement':
            return load_and_requirement(requirement_data)
        elif type_name == 'or_requirement':
            return load_or_requirement(requirement_data)
        else:
            print('ERROR: No course requirement "{}"'.format(type_name))
            return None

        # Input: row from the CourseRequirements table in the db for a completed course requirement
        # Return: The relevant requirement
        def load_completed_course_requirement(self, requirement_data: Tuple) -> Optional['completedCourseReq.CompletedCourseReq']:
            min_mark = requirement_data['min_mark']
            course_id = requirement_data['course_id']

            required_course = self.load_course(course_id, need_requirements=False)

            if required_course is None:
                print('ERROR: failed to get course with id {}'.format(course_id))
                return None

            return completedCourseReq.CompletedCourseReq(required_course, min_mark)

        # Input: row from the CourseRequirements table in the db for a current degree requirement
        # Return: The relevant requirement
        def load_current_degree_requirement(self, requirement_data: Tuple) -> Optional['degree.Degree']:
            degree_id = requirement_data['degree_id']

            required_degree = self.load_degree(degree_id, need_requirements=False)
            
            if required_degree is None:
                print('ERROR: No degree with id {}', degree_id)
                return None

            return enrollmentReq.EnrollmentReq(required_degree)

        def load_year_requirement(self, requirement_data: Tuple) -> 'yearReq.yearReq':
            year = requirement_data['year']

            return yearReq.YearReq(year)

        #def load_uoc_requirement(self, requirement_data: Tuple)
        #def load_and_requirement(self, requirement_data: Tuple)
        #def load_or_requirement(self, requirement_data: Tuple)


