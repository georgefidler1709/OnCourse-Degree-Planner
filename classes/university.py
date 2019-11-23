'''
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

university.py
Implementation of the University class which is a database of courses and programs

[MORE INFO ABOUT CLASS]
'''

from typing import Callable, Dict, List, Optional, Set, Tuple
from mypy_extensions import DefaultArg
from sqlite3 import Row, Connection

from . import  (
    andFilter,
    andReq,
    api,
    course,
    courseReq,
    courseFilter,
    degree,
    minDegreeReq,
    enrollmentReq,
    fieldFilter,
    freeElectiveFilter,
    genEdFilter,
    levelFilter,
    orFilter,
    orReq,
    specificCourseFilter,
    subjectReq,
    term,
    unparsedReq,
    wamReq,
    uocReq,
    yearReq,
)

class University(object):

    def __init__(self, query_db: Callable[[str, DefaultArg(Tuple), DefaultArg(bool, 'one')], Row]):
        # need to decide how degree/course details passed in
        # unpack and create degree.Degree and course.Course objects
        self.query_db = query_db
        self.course_requirement_types = self.load_course_requirement_types()
        self.course_filter_types = self.load_course_filter_types()

        # cache of courses loaded from the db for this session, indexed by database id
        self.courses: Dict[int, 'course.Course'] = {}
        # cache of degrees loaded from the db for this session, indexed by numeric code (which is
        # also db id)
        self.degrees: Dict[Tuple[int, int], 'degree.Degree'] = {}

    # Input: degree letter code (eg. COMPA1)
    # Return: corresponding degree.Degree object
    def find_degree_alpha_code(self, letter_code: str, year: int) -> Optional['degree.Degree']:
        response = self.query_db('''select id
                                 from Degrees
                                 where code = ?''', (letter_code,), one=True)
        if response is None:
            # No degree with that code, so return nothing
            return None
        else:
            numeric_code = response[0]
            self.assert_no_nulls(numeric_code)

            return self.find_degree_number_code(numeric_code, year)

    # Input: degree numerical code (eg. 3778)
    # Return: corresponding Degree object
    def find_degree_number_code(self, numeric_code: int, year: int) -> Optional['degree.Degree']:
        return self.load_degree(numeric_code, need_requirements=True, year=year)

    # Input: degree numerical code (eg. 3778), whether we need the requirements for the degree
    # (eg. if we're just loading the degree as part of a course requirement we don't need the
    # requirements)
    # assumes that you want the degree for 2020 unless you specify
    # Return: corresponding Degree object
    def load_degree(self, numeric_code: int, need_requirements: bool=True, year: int=2020) -> Optional['degree.Degree']:
        if numeric_code in self.degrees:
            # TODO: Might not work if we first load without requirements then call this with
            # requirements, decide whether we even want the need_requirements option anymore
            return self.degrees[(numeric_code, year)]

        response = self.query_db('''select name, faculty, duration
                                 from Degrees
                                 where id = ?''', (numeric_code,), one=True)

        if response is None:
            # No degree with that code, so return nothing
            return None

        name, faculty, duration = response
        self.assert_no_nulls(name, faculty, duration)

        alpha_code = 'ALPHA_CODE'

        # Check that there is actually an offering for that degree
        response = self.query_db('''select *
                                    from DegreeOfferings
                                    where degree_id = ?
                                    and year = ?''', (numeric_code, year), one=True)

        if response is None:
            # No offering for that year
            return None

        # get any notes on the degree
        response = self.query_db('''select note
                                from DegreeOfferingNotes
                                where offering_degree_id = ?
                                and offering_year_id = ?''',
                                (numeric_code, year))
        notes = []
        if response:
            for r in response:
                notes.append(r['note'])

        # create a degree without requirements, then add requirements later
        # This is done so that we can cache the degree, to avoid circular loading

        result_degree = degree.Degree(numeric_code, name, year, duration, faculty, [], alpha_code, notes)

        self.degrees[(numeric_code, year)] = result_degree

        requirements = []

        if need_requirements:
            # Get all of the requirements for the degree
            response = self.query_db('''select uoc_needed, requirement_id, alt_text
                                     from DegreeOfferingRequirements
                                     where offering_degree_id = ?
                                     and offering_year_id = ?''', (numeric_code, year))
            for offering_requirement in response:
                uoc, filter_id, alt_text = offering_requirement
                self.assert_no_nulls(uoc)

                if filter_id is None:
                    requirement = minDegreeReq.MinDegreeReq(None, uoc, alt_text)
                else:
                    filter = self.load_course_filter(filter_id)
                    self.assert_no_nulls(filter)

                    # mypy doesn't recognise that assert_no_nulls makes sure that filter is not none
                    assert filter is not None

                    requirement = minDegreeReq.MinDegreeReq(filter, uoc, alt_text)
                requirements.append(requirement)

        result_degree.requirements = requirements

        return result_degree

    # Input: course code (eg. COMP1511)
    # Return: corresponding Course object from courses
    def find_course(self, code: str, allow_unfinished: bool=False) -> Optional['course.Course']:
        subject = code[:4]
        numeric_code = code[4:]

        response = self.query_db('''select id
                                 from Courses
                                 where letter_code = ?
                                 and number_code = ?''', (subject, numeric_code), one=True)
        if response is None:
            return None
        else:
            self.assert_no_nulls(*response)
            (course_id, ) = response
            return self.load_course(course_id, allow_unfinished=allow_unfinished)

    # Input: course subject (eg. COMP), numeric code (eg. 1511) and whether we need the requirements
    # (same as for load_degree)
    # Return: corresponding Course object
    def load_course(self, course_id: int, allow_unfinished: bool, need_requirements: bool=True) -> Optional['course.Course']:
        if course_id in self.courses:
            # TODO: as with degrees, determine if need_requirements is even a useful argument
            desired_course = self.courses[course_id]
            if (not allow_unfinished) and (not desired_course.finished):
                return None

            return self.courses[course_id]

        response = self.query_db('''select letter_code, number_code, name, faculty, units, prereq,
        coreq, finished
                                 from Courses
                                 where id = ?''', (course_id, ), one=True)

        if response is None:
            # No matching course
            return None

        subject, numeric_code, name, faculty, units, prereq_id, coreq_id, finished = response
        # prereq, coreq, exclusion can each be null so we don't want to assert it
        self.assert_no_nulls(subject, numeric_code, name, faculty, units, finished)

        if (not allow_unfinished) and (not finished):
            # Course was not properly parsed, don't return it
            return None

        # Get the terms that the course runs in
        response = self.query_db('''select session_year, session_term
                                 from CourseOfferings
                                 where course_id = ?''', (course_id, ))
        terms = []
        for year, term_num in response:
            self.assert_no_nulls(year, term_num)
            terms.append(term.Term(year, term_num))

        result_course = course.Course(subject, numeric_code, name, units, terms, faculty,
                finished=finished)
        self.courses[course_id] = result_course

        if need_requirements:
            result_course.prereqs = self.load_course_requirement(prereq_id)
            result_course.coreqs = self.load_course_requirement(coreq_id)

            exclusion_ids = self.query_db('''select first_course, second_course
                                             from ExcludedCourses
                                             where first_course = ?
                                             or second_course = ?''', (course_id, course_id))

            exclusions = self.get_courses_from_relation(course_id, exclusion_ids)

            for exclusion in exclusions:
                result_course.add_exclusion(exclusion.course_code)

            equivalent_ids = self.query_db('''select first_course, second_course
                                            from EquivalentCourses
                                            where first_course = ?
                                            or second_course = ?''', (course_id, course_id))

            equivalents = self.get_courses_from_relation(course_id, equivalent_ids)
            for equivalent in equivalents:
                result_course.add_equivalent(equivalent.course_code)

        return result_course

    def get_courses_from_relation(self, course_id: int, other_ids: Row) -> List['course.Course']:
        courses = []

        for first_course_id, second_course_id in other_ids:
            self.assert_no_nulls(first_course_id, second_course_id)
            if first_course_id != course_id:
                other_id = first_course_id
            else:
                other_id = second_course_id

            other_course = self.load_course(other_id, allow_unfinished=True)
            if other_course is None:
                raise ValueError(f'No course with id {other_id}')

            courses.append(other_course)

        return courses




    # Input: A filter string [ITEMISE THESE HERE]
    # Return: List of courses that match the requested filter
    def filter_courses(self, course_filter: 'courseFilter.CourseFilter',
                degree: 'degree.Degree', eq: bool=True) -> List['course.Course']:
        # TODO: Smart loading that only loads relevant courses from the database
        response = self.query_db('''select id from Courses where finished = 1''')
        course_ids = list(map(lambda x: x[0], response))

        self.assert_no_nulls(*course_ids)

        courses = list(map(lambda x: self.load_course(x, allow_unfinished=False), course_ids))

        self.assert_no_nulls(*courses)
        matching = list(filter(lambda x: x is not None and course_filter.accepts_course(x, degree, eq),
            courses))

        self.assert_no_nulls(*matching)

        # mypy does not recognise that the filter only includes non-optional courses, so do another
        # filter to explicitly only include non-Nones
        to_return = []
        for course in matching:
            if course is not None:
                to_return.append(course)

        return to_return

    # Return: A dictionary containing the ids of each course requirement type along with their names
    def load_course_requirement_types(self) -> Dict[int, str]:
        requirement_types: Dict[int, str] = {}
        response = self.query_db('''select id, name
                                 from CourseRequirementTypes''')

        for requirement_type in response:
            self.assert_no_nulls(*requirement_type)
            type_id, type_name = requirement_type
            requirement_types[type_id] = type_name

        return requirement_types

    # Return: A dictionary containing the ids of each course filter type along with their names
    def load_course_filter_types(self) -> Dict[int, str]:
        filter_types: Dict[int, str] = {}
        response = self.query_db('''select id, name
                                 from CourseFilterTypes''')

        for filter_type in response:
            self.assert_no_nulls(*filter_type)
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
            print('ERROR: No course requirement {}'.format(requirement_id))
            return None

        requirement_data = response
        type_id = requirement_data['type_id']
        type_name = self.course_requirement_types.get(type_id, None)

        self.assert_no_nulls(type_id, type_name)

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
        elif type_name == 'UnparsedRequirement':
            return self.load_unparsed_requirement(requirement_data)
        elif type_name == 'WamRequirement':
            return self.load_wam_requirement(requirement_data)
        else:
            print('ERROR: No course requirement \'{}\''.format(type_name))
            return None

    # Input: row from the CourseRequirements table in the db for a completed course requirement
    # Return: The relevant requirement
    def load_completed_course_requirement(self, requirement_data: Row) -> Optional['subjectReq.SubjectReq']:
        min_mark = requirement_data['min_mark']
        course_id = requirement_data['course_id']

        required_course = self.load_course(course_id, allow_unfinished=True)

        if required_course is None:
            print('ERROR: failed to get course with id {}'.format(course_id))
            return None

        return subjectReq.SubjectReq(required_course, min_mark)

    # Input: row from the CourseRequirements table in the db for a current degree requirement
    # Return: The relevant requirement
    def load_current_degree_requirement(self, requirement_data: Row) -> Optional['courseReq.CourseReq']:
        degree_id = requirement_data['degree_id']

        response = self.query_db('''select name
                                    from Degrees
                                    where id = ?''', (degree_id, ), one=True)

        if response is None:
            # No degree with that id
            print('ERROR: failed to get degree with id {}'.format(degree_id))
            return None

        (degree_name, ) = response

        return enrollmentReq.EnrollmentReq(degree_id, degree_name)

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

        if course_filter_id is None:
            # overall requirement, no filter
            return uocReq.UOCReq(uoc, None)

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
            self.assert_no_nulls(*result)
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
            self.assert_no_nulls(*result)
            (child_id, ) = result

            child = self.load_course_requirement(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return orReq.OrReq(children)

    def load_unparsed_requirement(self, requirement_data: Row) -> 'unparsedReq.UnparsedReq':
        requirement_string = requirement_data['requirement_string']

        return unparsedReq.UnparsedReq(requirement_string)

    def load_wam_requirement(self, requirement_data: Row) -> 'wamReq.WAMReq':
        wam = requirement_data['wam']

        return wamReq.WAMReq(wam)

    # Input: the id of the course filter
    # Return: The course filter in question
    def load_course_filter(self, filter_id: int) -> Optional['courseFilter.CourseFilter']:
        response = self.query_db('''select *
                                 from CourseFilters
                                 where id = ?''', (filter_id, ), one=True)

        if response is None:
            # Failed to load course filter
            raise ValueError(f'ERROR: No course filter {filter_id}')

        filter_data = response
        type_id = filter_data['type_id']
        type_name = self.course_filter_types.get(type_id, None)

        self.assert_no_nulls(type_id, type_name)

        if type_name is None:
            # Invalid course filter type
            print('ERROR: invalid course filter type {}'.format(type_id))
            return None

        # Determine which filter type it is from the name
        if type_name == 'SpecificCourseFilter':
            return self.load_specific_course_filter(filter_data)
        elif type_name == 'GenEdFilter':
            return self.load_gen_ed_filter(filter_data)
        elif type_name == 'FieldFilter':
            return self.load_field_filter(filter_data)
        elif type_name == 'LevelFilter':
            return self.load_level_filter(filter_data)
        elif type_name == 'FreeElectiveFilter':
            return self.load_free_elective_filter(filter_data)
        elif type_name == 'AndFilter':
            return self.load_and_filter(filter_data)
        elif type_name == 'OrFilter':
            return self.load_or_filter(filter_data)
        else:
            print('ERROR: No course filter \'{}\''.format(type_name))
            return None

    # Input: row from the CourseFilters table in the db for a specific course filter
    # Return: The relevant filter
    def load_specific_course_filter(self, filter_data: Row) -> Optional['specificCourseFilter.SpecificCourseFilter']:
        course_id = filter_data['course_id']

        allowed_course = self.load_course(course_id, allow_unfinished=True)

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

    def load_level_filter(self, filter_data: Row) -> 'levelFilter.LevelFilter':
        level = filter_data['level']
        return levelFilter.LevelFilter(level)

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
            self.assert_no_nulls(*result)
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
            self.assert_no_nulls(*result)
            (child_id, ) = result
            child = self.load_course_filter(child_id)
            if child is None:
                print('ERROR: no child with id {}'.format(child_id))
            else:
                children.append(child)

        return orFilter.OrFilter(children)

    # Return: Jsonifiable dict that contains minimal data to display to the user in a menu
    def get_simple_degrees(self) -> api.SimpleDegrees:
        response = self.query_db('''select degree.id, degree.name, offering.year
                                 from DegreeOfferings as offering
                                 join Degrees as degree
                                 on degree.id = offering.degree_id
                                 order by degree.id, offering.year''')

        degrees: List[api.SimpleDegree] = []
        years: Set[str] = set()

        current_id: str = ''
        current_name: str = ''
        current_years: List[str] = []

        for offering in response:
            degree_id, name, year = offering
            degree_id = str(degree_id)

            if current_id != degree_id:
                # Don't add if the current degree is just the empty data for the first run through
                if current_id != '':
                    degrees.append({'id': current_id, 'years': current_years, 'name': current_name})

                current_id = degree_id
                current_name = name
                current_years = []

            current_years.append(year)

            years.add(year)

        if current_id != '':
            # Add the final degree
            degrees.append({'id': current_id, 'years': current_years, 'name': current_name})

        years_list = list(sorted(years))

        return {'degrees': degrees, 'years': years_list}

    def get_simple_courses(self) -> api.SimpleCourses:
        response = self.query_db('''select letter_code, number_code, name
                                 from Courses where finished = 1''')
        return [{'id': i['letter_code'] + i['number_code'], 'name': i['name']} for i in response];

    # get the course information with terms so you can display to user when courses are offered
    def get_full_courses(self) -> api.CourseList:
        # get the ids of all courses in database
        responses = self.query_db('''select id from Courses where finished = 1''')

        # now load the full course data using load_course logic
        res: api.CourseList = []

        for r in responses:
            new = self.load_course(r['id'], allow_unfinished=True, need_requirements=True)
            if new is None:
                continue

            res.append(new.to_api())

        return res


    # Assert that a sequence of arguments contains no None values
    def assert_no_nulls(self, *args):
        for i, arg in enumerate(args):
            if arg is None:
                raise ValueError(f'ERROR: argument #{i} is None in arguments {args}')
