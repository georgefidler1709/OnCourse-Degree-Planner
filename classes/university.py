"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

university.py
Implementation of the University class which is a database of courses and programs

[MORE INFO ABOUT CLASS]
"""

from typing import Dict, List, Optional, Callable, Tuple
from sqlite3 import Row, Connection

from . import andFilter
from . import andReq
from . import course
from . import courseReq
from . import courseFilter
from . import degree
from . import degreeReq
from . import enrollmentReq
from . import fieldFilter
from . import freeElectiveFilter
from . import genEdFilter
from . import orFilter
from . import orReq
from . import specificCourseFilter
from . import subjectReq
from . import term
from . import uocReq
from . import yearReq
from . import api

# Temporary: only allow 2019 results
YEAR = 2019

class University(object):

    def __init__(self, query_db: Callable[[str, Tuple, bool], Tuple]):
        # need to decide how degree/course details passed in
        # unpack and create degree.Degree and course.Course objects
        self.query_db = query_db
        self.course_requirement_types = self.load_course_requirement_types()
        self.course_filter_types = self.load_course_filter_types()

    # Input: degree letter code (eg. COMPA1)
    # Return: corresponding degree.Degree object
    def find_degree_alpha_code(self, letter_code: str) -> Optional['degree.Degree']:
        response = self.query_db('''select id
                                 from Degrees
                                 where code = ?''', (letter_code,), one=True)
        if response is None:
            # No degree with that code, so return nothing
            return None
        else:
            numeric_code = response[0]
            return self.find_degree_number_code(numeric_code)

    # Input: degree numerical code (eg. 3778)
    # Return: corresponding Degree object
    def find_degree_number_code(self, numeric_code: int) -> Optional['degree.Degree']:
        return self.load_degree(numeric_code, need_requirements = True)

    # Input: degree numerical code (eg. 3778), whether we need the requirements for the degree
    # (eg. if we're just loading the degree as part of a course requirement we don't need the
    # requirements)
    # Return: corresponding Degree object
    def load_degree(self, numeric_code: int, need_requirements: bool=True) -> Optional['degree.Degree']:
        year = YEAR
        response = self.query_db('''select name, code
                                 from Degrees
                                 where id = ?''', (numeric_code,), one=True)

        if response is None:
            # No degree with that code, so return nothing
            return None

        name, alpha_code = response

        # Get all of the requirements for the degree
        response = self.query_db('''select uoc_needed, requirement_id
                                 from DegreeOfferingRequirements
                                 where offering_degree_id = ?
                                 and offering_year_id = ?''', (numeric_code, year))

        requirements = []

        print("Response is")
        print(response)
        print("\n\n\n")

        if need_requirements:
            for offering_requirement in response:
                uoc, filter_id = offering_requirement
                filter = self.load_course_filter(filter_id)

                if filter is not None:
                    requirement = degreeReq.DegreeReq(filter, uoc)
                    requirements.append(requirement)
                else:
                    # Filter should not be None
                    print("ERROR: filter {} for degree requirement should not be null".format(filter_id))
        
        # TODO: put duration in database
        duration = 3
        return degree.Degree(numeric_code, name, year, duration, requirements)

    # Input: course code (eg. COMP1511)
    # Return: corresponding Course object from courses
    def find_course(self, code: str) -> Optional['course.Course']:
        subject = code[:4]
        numeric_code = code[4:]

        response = self.query_db('''select id
                                 from Courses
                                 where letter_code = ?
                                 and number_code = ?''', (subject, numeric_code), one=True)
        if response is None:
            return None
        else:
            (course_id, ) = response
            return self.load_course(course_id, need_requirements=True)

    # Input: course subject (eg. COMP), numeric code (eg. 1511) and whether we need the requirements
    # (same as for load_degree)
    # Return: corresponding Course object
    def load_course(self, course_id: int, need_requirements: bool=True) -> Optional['course.Course']:
        response = self.query_db('''select letter_code, number_code, name, units, prereq, coreq, exclusion
                                 from Courses
                                 where id = ?''', (course_id, ), one=True)

        if response is None:
            # No matching course
            return None

        subject, numeric_code, name, units, prereq_id, coreq_id, exclusion_id = response

        # Get the terms that the course runs in
        response = self.query_db('''select session_year, session_term
                                 from CourseOfferings
                                 where course_id = ?''', (course_id, ))
        terms = []
        for year, term_num in response:
            terms.append(term.Term(year, term_num))

        if need_requirements:
            prereq = self.load_course_requirement(prereq_id)
            coreq = self.load_course_requirement(coreq_id)
            exclusion = self.load_course_requirement(exclusion_id)
        else:
            prereq = None
            coreq = None
            exclusion = None

        return course.Course(subject, numeric_code, name, units, terms, prereq, coreq, exclusion)

    # Input: A filter string [ITEMISE THESE HERE]
    # Return: List of courses that match the requested filter
    def filter_courses(self, filter: 'courseFilter.CourseFilter') -> List['course.Course']:
        # TODO
        pass

    # Return: A dictionary containing the ids of each course requirement type along with their names
    def load_course_requirement_types(self) -> Dict[int, str]:
        requirement_types: Dict[int, str] = {}
        response = self.query_db('''select id, name
                                 from CourseRequirementTypes''')

        for requirement_type in response:
            type_id, type_name = requirement_type
            requirement_types[type_id] = type_name

        return requirement_types

    # Return: A dictionary containing the ids of each course filter type along with their names
    def load_course_filter_types(self) -> Dict[int, str]:
        filter_types: Dict[int, str] = {}
        response = self.query_db('''select id, name
                                 from CourseFilterTypes''')

        for filter_type in response:
            type_id, type_name = filter_type
            filter_types[type_id] = type_name

        return filter_types

    # Input: the id of the course requirement
    # Return: The course requirement in question
    def load_course_requirement(self, requirement_id: int) -> Optional['courseReq.CourseReq']:
        if requirement_id is None:
            # Courses might not have prereqs/coreqs/exclusions
            return None

        response = self.query_db('''select *
                                 from CourseRequirements
                                 where id = ?''', (requirement_id, ), one=True)

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

        # Determine which requirement type it is from the name
        if type_name == 'CompletedCourseRequirement':
            return self.load_completed_course_requirement(requirement_data)
        elif type_name == 'CurrentDegreeRequirement':
            return self.load_current_degree_requirement(requirement_data)
        elif type_name == 'YearRequirement':
            return self.load_year_requirement(requirement_data)
        elif type_name == 'UocRequirement':
            return self.load_uoc_requirement(requirement_data)
        elif type_name == 'AndRequirement':
            return self.load_and_requirement(requirement_data)
        elif type_name == 'OrRequirement':
            return self.load_or_requirement(requirement_data)
        else:
            print('ERROR: No course requirement "{}"'.format(type_name))
            return None

    # Input: row from the CourseRequirements table in the db for a completed course requirement
    # Return: The relevant requirement
    def load_completed_course_requirement(self, requirement_data: Row) -> Optional['subjectReq.SubjectReq']:
        min_mark = requirement_data['min_mark']
        course_id = requirement_data['course_id']

        required_course = self.load_course(course_id, need_requirements=False)

        if required_course is None:
            print('ERROR: failed to get course with id {}'.format(course_id))
            return None

        return subjectReq.SubjectReq(required_course, min_mark)

    # Input: row from the CourseRequirements table in the db for a current degree requirement
    # Return: The relevant requirement
    def load_current_degree_requirement(self, requirement_data: Row) -> Optional['courseReq.CourseReq']:
        degree_id = requirement_data['degree_id']

        required_degree = self.load_degree(degree_id, need_requirements=False)

        if required_degree is None:
            print('ERROR: No degree with id {}', degree_id)
            return None

        return enrollmentReq.EnrollmentReq(required_degree)
    
    # Input: row from the CourseRequirements table in the db for a year requirement
    # Return: The relevant requirement
    def load_year_requirement(self, requirement_data: Row) -> 'yearReq.YearReq':
        year = requirement_data['year']

        return yearReq.YearReq(year)

    # Input: row from the CourseRequirements table in the db for a uoc requirement
    # Return: The relevant requirement
    def load_uoc_requirement(self, requirement_data: Row) -> 'uocReq.UOCReq':
        uoc = requirement_data['uoc_amount_required']
        min_level = requirement_data['uoc_min_level']
        subject = requirement_data['uoc_subject']
        course_filter_id = requirement_data['uoc_course_filter']

        filter = self.load_course_filter(course_filter_id)
        if filter is None:
            print('ERROR: no course filter with id {}'.format(course_filter_id))

        return uocReq.UOCReq(uoc, filter)

    # Input: row from the CourseRequirements table in the db for an and requirement
    # Return: The relevant requirement
    def load_and_requirement(self, requirement_data: Row) -> 'andReq.AndReq':
        requirement_id = requirement_data['id']
        results = self.query_db('''select child_id
                                from CourseRequirementHierarchies
                                where parent_id = ?''', (requirement_id, ))
        children = []
        for result in results:
            (child_id, ) = result
            child = self.load_course_requirement(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return andReq.AndReq(children)

    # Input: row from the CourseRequirements table in the db for an or requirement
    # Return: The relevant requirement
    def load_or_requirement(self, requirement_data: Row) -> 'orReq.OrReq':
        requirement_id = requirement_data['id']
        results = self.query_db('''select child_id
                                from CourseRequirementHierarchies
                                where parent_id = ?''', (requirement_id, ))
        children = []
        for result in results:
            (child_id, ) = result
            child = self.load_course_requirement(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return orReq.OrReq(children)

    # Input: the id of the course filter
    # Return: The course filter in question
    def load_course_filter(self, filter_id: int) -> Optional['courseFilter.CourseFilter']:
        response = self.query_db('''select *
                                 from CourseFilters
                                 where id = ?''', (filter_id, ), one=True)

        if response is None:
            # Failed to load course filter
            print("ERROR: No course filter {}".format(filter_id))
            return None

        filter_data = response
        type_id = filter_data['type_id']
        type_name = self.course_filter_types.get(type_id, None)
        if type_name is None:
            # Invalid course filter type
            print("ERROR: invalid course filter type {}".format(type_id))
            return None

        # Determine which filter type it is from the name
        if type_name == 'SpecificCourseFilter':
            return self.load_specific_course_filter(filter_data)
        elif type_name == 'GenEdFilter':
            return self.load_gen_ed_filter(filter_data)
        elif type_name == 'FieldFilter':
            return self.load_field_filter(filter_data)
        elif type_name == 'FreeElectiveFilter':
            return self.load_free_elective_filter(filter_data)
        elif type_name == 'AndFilter':
            return self.load_and_filter(filter_data)
        elif type_name == 'OrFilter':
            return self.load_or_filter(filter_data)
        else:
            print('ERROR: No course filter "{}"'.format(type_name))
            return None

    # Input: row from the CourseFilters table in the db for a specific course filter
    # Return: The relevant filter
    def load_specific_course_filter(self, filter_data: Row) -> Optional['specificCourseFilter.SpecificCourseFilter']:
        min_mark = filter_data['min_mark']
        course_id = filter_data['course_id']

        allowed_course = self.load_course(course_id, need_requirements=False)

        if allowed_course is None:
            print('ERROR: failed to get course with id {}'.format(course_id))
            return None

        return specificCourseFilter.SpecificCourseFilter(allowed_course)


    # Input: row from the CourseFilters table in the db for a gen ed filter
    # Return: The relevant filter
    def load_gen_ed_filter(self, filter_data: Row) -> 'genEdFilter.GenEdFilter':
        return genEdFilter.GenEdFilter()

    # Input: row from the CourseFilters table in the db for a field filter
    # Return: The relevant filter
    def load_field_filter(self, filter_data: Row) -> 'fieldFilter.FieldFilter':
        field_code = filter_data['field_code']
        return fieldFilter.FieldFilter(field_code)

    # Input: row from the CourseFilters table in the db for a free elective filter
    # Return: The relevant filter
    def load_free_elective_filter(self, filter_data: Row) -> 'freeElectiveFilter.FreeElectiveFilter':
        return freeElectiveFilter.FreeElectiveFilter()

    # Input: row from the CourseFilters table in the db for an and filter
    # Return: The relevant filter
    def load_and_filter(self, filter_data: Row) -> 'andFilter.AndFilter':
        filter_id = filter_data['id']
        results = self.query_db('''select child_id
                                from CourseFilterHierarchies
                                where parent_id = ?''', (filter_id, ))
        children = []
        for result in results:
            (child_id, ) = result
            child = self.load_course_filter(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return andFilter.AndFilter(children)


    # Input: row from the CourseFilters table in the db for an or filter
    # Return: The relevant filter
    def load_or_filter(self, filter_data: Row) -> 'orFilter.OrFilter':
        filter_id = filter_data['id']
        results = self.query_db('''select child_id
                                from CourseFilterHierarchies
                                where parent_id = ?''', (filter_id, ))
        children = []
        for result in results:
            (child_id, ) = result
            child = self.load_course_filter(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return orFilter.OrFilter(children)

    # Return: Jsonifiable dict that contains minimal data to display to the user in a menu
    def get_simple_degrees(self) -> api.SimpleDegrees:
        response = self.query_db('''select name, code
                                 from Degrees''')
        return [apiTypes.SimpleDegree(id=i['code'], name=i['name']) for i in response];
