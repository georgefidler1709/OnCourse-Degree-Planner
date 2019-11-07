"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_university.py
Test the functions defined in university.py

"""

import pytest
import sqlite3
from typing import Tuple, Optional

from classes import university, course, degree, andFilter, andReq, courseFilter, courseReq
from classes import degreeReq, enrollmentReq, fieldFilter, freeElectiveFilter, genEdFilter
from classes import levelFilter, orFilter, orReq, specificCourseFilter, subjectReq, uocReq, yearReq

class DbHelper:
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

    def query_db(self, query : str, args: Tuple = (), one = False) -> Tuple:
        # query function from flask documentation
        # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

        cur = self.cursor.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv

    def get_requirement_type_id(self, name: str) -> Optional[int]:
        response = self.query_db('''select id from CourseRequirementTypes where name = ?''', (name,), one=True)
        if response is None:
            return None
        else:
            return response[0]

    def get_filter_type_id(self, name: str) -> Optional[int]:
        response = self.query_db('''select id from CourseFilterTypes where name = ?''', (name, ), one=True)
        if response is None:
            return None
        else:
            return response[0]

    # Inserts a degree into the database
    # Ignores requirements
    def insert_degree(self, degree):
        self.insert_degree_from_fields(degree.name, degree.alpha_code, degree.num_code, degree.year,
                degree.requirements)

    # Inserts a degree into the database from the fields that make it up
    # Ignores requirements
    def insert_degree_from_fields(self, name='TestDegree', code='TestCode', id=42, year=2019, requirements=[]):
        self.cursor.execute('insert into Degrees(name, code, id) values(?, ?, ?)', (name, code, id))

        self.cursor.execute('insert into DegreeOfferings(year, degree_id) values(?, ?)', (year, id))

    # Inserts a course into the database
    # Ignores the terms it runs in or any prereqs/coreqs/exclusions/equivalents
    def insert_course(self, course, prereq=None, coreq=None, exclusion=None, equivalents=[]):
        return self.insert_course_from_fields(course.subject, course.code, course.level, course.name, course.units,
                prereq, coreq, exclusion, equivalents)

    # Inserts a course from just the fields that make up the course
    def insert_course_from_fields(self, letter_code='COMP', number_code='1511', level=1,
            name='Intro to computing', units=6, prereq=None, coreq=None, exclusion=None,
            equivalents=[]):
        self.cursor.execute('''insert into Courses(letter_code, number_code, level, name, units,
        prereq, coreq, exclusion) values (?, ?, ?, ?, ?, ?, ?, ?)''',
        (letter_code, number_code, level, name, units, prereq, coreq, exclusion))

        id = self.cursor.lastrowid

        for equivalent_id in equivalents:
            if id < equivalent_id:
                first_course = id
                second_course = equivalent_id
            else:
                first_course = equivalent_id
                second_course = id
            self.cursor.execute('''insert or ignore into EquivalentCourses(first_course, second_course)
            values(?, ?)''', (first_course, second_course))

        return id

    def insert_degree_requirement(self, degree, filter_id, uoc_needed):
        self.cursor.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
        offering_year_id, requirement_id, uoc_needed) values(?, ?, ?, ?)''', (degree.num_code,
            degree.year, filter_id, uoc_needed))

class TestUniversityWithDb():
    def setup_method(self, function):
        self.db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

        self.cursor = self.db.cursor()

        with open('server/db/schema.sql') as f:
            self.db.executescript(f.read())

        with open('server/db/setup_enums.sql') as f:
            self.db.executescript(f.read())

        self.h = DbHelper(self.db)

        self.university = university.University(self.h.query_db)

        self.first_course = course.Course("TEST", 1000, "Test course 1", 6, [])
        self.second_course = course.Course("COMP", 2521, "Test course 2", 3, [])

        # TODO: check different years
        self.first_degree = degree.Degree(1111, "Test degree", 2019, 3, [], "ABCDE")

        self.second_degree = degree.Degree(3223, "Test degree 2", 2019, 5, [], "FGHIJ")

    def teardown_method(self, function):
        self.db.close()

class TestUniversity_FindDegreeNumberCode(TestUniversityWithDb):
    def test_no_degrees(self):
        degree = self.university.find_degree_number_code(1)

        assert degree is None

    def test_single_degree(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)
        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 0
        assert degree.name == input_degree.name
        assert degree.year == input_degree.year

    def test_single_degree_no_match(self):
        input_degree = self.first_degree

        incorrect_id = input_degree.num_code + 1
        self.h.insert_degree(input_degree)

        degree = self.university.find_degree_number_code(incorrect_id)

        assert degree is None

    def test_multiple_degrees(self):
        first_degree = self.first_degree

        self.h.insert_degree(first_degree)


        second_degree = self.second_degree
        self.h.insert_degree(second_degree)
        degree = self.university.find_degree_number_code(first_degree.num_code)

        assert degree is not None
        assert degree.name == first_degree.name

    def test_degree_with_specific_course_filter(self):
        input_degree = self.first_degree
        self.h.insert_degree(input_degree)

        input_course = self.first_course

        course_id = self.h.insert_course(input_course)

        filter_type_id = self.h.get_filter_type_id('SpecificCourseFilter')
        print(filter_type_id)

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id, min_mark, course_id) values(?, ?,
        ?)''', (filter_type_id, mark_needed, course_id))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'SpecificCourseFilter'
        assert filter.course == input_course

    def test_degree_with_specific_course_filter_with_prereq(self):
        input_degree = self.first_degree
        self.h.insert_degree(input_degree)

        input_course = self.first_course

        prereq_year = 1
        prereq_type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (prereq_type_id, prereq_year))

        prereq_id = self.cursor.lastrowid


        course_id = self.h.insert_course(input_course, prereq=prereq_id)

        filter_type_id = self.h.get_filter_type_id('SpecificCourseFilter')
        print(filter_type_id)

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id, min_mark, course_id) values(?, ?,
        ?)''', (filter_type_id, mark_needed, course_id))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'SpecificCourseFilter'
        assert filter.course == input_course
        prereq = filter.course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == prereq_year

    def test_degree_with_gen_ed_filter(self):
        input_degree = self.first_degree
        self.h.insert_degree(input_degree)

        filter_type_id = self.h.get_filter_type_id('GenEdFilter')
        print(filter_type_id)

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'GenEdFilter'

    def test_degree_with_field_filter(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        filter_type_id = self.h.get_filter_type_id('FieldFilter')
        field = 'COMP'
        level = 2

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id, field_code, level) values(?, ?,
                ?)''', (filter_type_id, field, level))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'FieldFilter'
        assert filter.field == field

    def test_degree_with_free_elective_filter(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'FreeElectiveFilter'


    def test_degree_with_and_filter(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        filter_type_id = self.h.get_filter_type_id('AndFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (sub_filter_type_id, ))

        sub_filter_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseFilterHierarchies(parent_id, child_id) values(?,
        ?)''', (filter_id, sub_filter_id))


        uoc_needed = 51

        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'AndFilter'
        sub_filters = filter.filters
        assert len(sub_filters) == 1
        sub_filter = sub_filters[0]
        assert sub_filter.filter_name == 'FreeElectiveFilter'

    def test_degree_with_or_filter(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        filter_type_id = self.h.get_filter_type_id('OrFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (sub_filter_type_id, ))

        sub_filter_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseFilterHierarchies(parent_id, child_id) values(?,
        ?)''', (filter_id, sub_filter_id))

        uoc_needed = 44


        self.h.insert_degree_requirement(input_degree, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(input_degree.num_code)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'OrFilter'
        sub_filters = filter.filters
        assert len(sub_filters) == 1
        sub_filter = sub_filters[0]
        assert sub_filter.filter_name == 'FreeElectiveFilter'


class TestUniversity_FindCourse(TestUniversityWithDb):
    def test_no_course(self):
        course = self.university.find_course('COMP1511')

        assert course is None

    def test_single_course(self):
        input_course = self.first_course

        self.h.insert_course(input_course)

        course = self.university.find_course(input_course.course_code)

        assert course == input_course
        assert len(course.equivalents) == 0

    def test_multiple_courses(self):
        first_course = self.first_course
        second_course = self.second_course

        self.h.insert_course(first_course)
        self.h.insert_course(second_course)

        course = self.university.find_course(first_course.course_code)

        assert course == first_course

    def test_course_with_completed_course_prereq(self):
        input_course = self.first_course

        required_course = self.second_course

        required_course_id = self.h.insert_course(required_course)


        type_id = self.h.get_requirement_type_id('CompletedCourseRequirement')
        min_mark = 75

        self.cursor.execute('''insert into CourseRequirements(type_id, min_mark, course_id)
        values(?, ?, ?)''', (type_id, min_mark, required_course_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CompletedCourseRequirement'
        inner_course = prereq.course
        assert inner_course == required_course

    def test_course_with_completed_course_prereq_with_inner_prereq(self):
        input_course = self.first_course

        required_course = self.second_course

        required_prereq_type_id = self.h.get_requirement_type_id('YearRequirement')
        required_prereq_year = 2
        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (required_prereq_type_id, required_prereq_year))
        required_prereq_id = self.cursor.lastrowid

        required_course_id = self.h.insert_course(required_course, prereq=required_prereq_id)


        type_id = self.h.get_requirement_type_id('CompletedCourseRequirement')
        min_mark = 75

        self.cursor.execute('''insert into CourseRequirements(type_id, min_mark, course_id)
        values(?, ?, ?)''', (type_id, min_mark, required_course_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CompletedCourseRequirement'
        inner_course = prereq.course
        assert inner_course == required_course
        inner_prereq = inner_course.prereqs
        assert inner_prereq is not None
        assert inner_prereq.requirement_name == 'YearRequirement'
        assert inner_prereq.year == required_prereq_year

    def test_course_with_circular_completed_course_prereq(self):
        input_course = self.first_course

        input_course_id = self.h.insert_course(input_course)


        type_id = self.h.get_requirement_type_id('CompletedCourseRequirement')
        min_mark = 75

        self.cursor.execute('''insert into CourseRequirements(type_id, min_mark, course_id)
        values(?, ?, ?)''', (type_id, min_mark, input_course_id))

        requirement_id = self.cursor.lastrowid

        self.cursor.execute('''update Courses set prereq = ?''', (requirement_id,))

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CompletedCourseRequirement'
        inner_course = prereq.course
        assert inner_course == course


    def test_course_with_degree_prereq(self):
        input_course = self.first_course

        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        type_id = self.h.get_requirement_type_id('CurrentDegreeRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, degree_id) values(?, ?)''',
                (type_id, input_degree.num_code))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CurrentDegreeRequirement'
        required_degree = prereq.degree
        assert required_degree is not None
        assert required_degree.num_code == input_degree.num_code
        assert required_degree.name == input_degree.name

    def test_course_with_year_prereq(self):
        input_course = self.first_course

        year = 2

        type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, year))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == year

    def test_course_with_uoc_prereq(self):
        input_course = self.first_course

        #Insert filter for the uoc requirement
        filter_type_id = self.h.get_filter_type_id('FieldFilter')
        filter_field = 'COMP'
        filter_level = 2

        self.cursor.execute('''insert into CourseFilters(type_id, field_code, level) values(?, ?,
                ?)''', (filter_type_id, filter_field, filter_level))

        filter_id = self.cursor.lastrowid

        # Insert requirement
        requirement_uoc_required = 12
        requirement_min_level = 3
        requirement_subject = 'COMP'

        requirement_type_id = self.h.get_requirement_type_id('UocRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, uoc_amount_required,
                uoc_min_level, uoc_subject, uoc_course_filter) values(?, ?, ?, ?, ?)''',
                (requirement_type_id, requirement_uoc_required, requirement_min_level,
                    requirement_subject, filter_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'UocRequirement'
        assert prereq.uoc == requirement_uoc_required
        filter = prereq.filter
        assert filter.filter_name == 'FieldFilter'

    def test_course_with_and_prereq(self):
        input_course = self.first_course

        year = 2

        sub_requirement_type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (sub_requirement_type_id, year))

        sub_requirement_id = self.cursor.lastrowid

        requirement_type_id =  self.h.get_requirement_type_id('AndRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id) values(?)''',
                (requirement_type_id,))

        requirement_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseRequirementHierarchies(parent_id, child_id)
        values(?, ?)''', (requirement_id, sub_requirement_id))

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'AndRequirement'
        sub_requirements = prereq.reqs
        assert len(sub_requirements) == 1
        sub_requirement = sub_requirements[0]
        assert sub_requirement.requirement_name == 'YearRequirement'

    def test_course_with_or_prereq(self):
        input_course = self.first_course

        year = 2

        sub_requirement_type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (sub_requirement_type_id, year))

        sub_requirement_id = self.cursor.lastrowid

        requirement_type_id = self.h.get_requirement_type_id('OrRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id) values(?)''',
                (requirement_type_id,))

        requirement_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseRequirementHierarchies(parent_id, child_id)
        values(?, ?)''', (requirement_id, sub_requirement_id))

        self.h.insert_course(input_course, prereq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'OrRequirement'
        sub_requirements = prereq.reqs
        assert len(sub_requirements) == 1
        sub_requirement = sub_requirements[0]
        assert sub_requirement.requirement_name == 'YearRequirement'

    def test_course_with_coreq(self):
        input_course = self.first_course

        year = 2

        type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, year))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, coreq=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        assert course.prereqs is None
        coreq = course.coreqs
        assert coreq is not None
        assert coreq.requirement_name == 'YearRequirement'
        assert coreq.year == year

    def test_course_with_exclusion(self):
        input_course = self.first_course

        required_course = self.second_course

        required_course_id = self.h.insert_course(required_course)


        type_id = self.h.get_requirement_type_id('CompletedCourseRequirement')
        min_mark = 50

        self.cursor.execute('''insert into CourseRequirements(type_id, min_mark, course_id)
        values(?, ?, ?)''', (type_id, min_mark, required_course_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(input_course, exclusion=requirement_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        exclusion = course.exclusions
        assert exclusion is not None
        assert exclusion.requirement_name == 'CompletedCourseRequirement'
        inner_course = exclusion.course
        assert inner_course == required_course

    def test_course_with_equivalents(self):
        input_course = self.first_course

        equivalent_course = self.second_course

        equivalent_id = self.h.insert_course(equivalent_course)

        self.h.insert_course(input_course, equivalents=[equivalent_id])

        course = self.university.find_course(input_course.course_code)

        assert course is not None
        assert len(course.equivalents) == 1
        equivalent = course.equivalents[0]
        assert equivalent == equivalent_course

    def test_course_with_prereq_and_coreq(self):
        input_course = self.first_course

        units = 50

        prereq_year = 2
        coreq_year = 4

        type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, prereq_year))

        prereq_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, coreq_year))

        coreq_id = self.cursor.lastrowid



        self.h.insert_course(input_course, prereq=prereq_id, coreq=coreq_id)

        course = self.university.find_course(input_course.course_code)

        assert course is not None

        coreq = course.coreqs
        assert coreq is not None
        assert coreq.requirement_name == 'YearRequirement'
        assert coreq.year == coreq_year

        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == prereq_year


class TestUniversity_FilterCourses(TestUniversityWithDb):
    def test_no_courses(self):
        filter = freeElectiveFilter.FreeElectiveFilter() 

        courses = self.university.filter_courses(filter)
        assert len(courses) == 0

    def test_single_matching_course(self):
        filter = freeElectiveFilter.FreeElectiveFilter()

        input_course = self.first_course

        self.h.insert_course(input_course)

        courses = self.university.filter_courses(filter)

        assert len(courses) == 1
        course = courses[0]
        course == input_course

    def test_single_nonmatching_course(self):
        filter = levelFilter.LevelFilter(2)

        input_course = self.first_course

        self.h.insert_course(input_course)

        courses = self.university.filter_courses(filter)

        assert len(courses) == 0

    def test_multiple_matching_courses(self):
        filter = freeElectiveFilter.FreeElectiveFilter()

        input_course = self.first_course

        self.h.insert_course(input_course)

        courses = self.university.filter_courses(filter)

        assert len(courses) == 1
        course = courses[0]
        assert course == input_course
    
    def test_specific_course_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        filter = specificCourseFilter.SpecificCourseFilter(self.first_course)

        courses = self.university.filter_courses(filter)

        assert len(courses) == 1
        course = courses[0]
        assert course == self.first_course

    def test_gen_ed_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        filter = genEdFilter.GenEdFilter()

        # TODO: Work out how we're determining gen ed filter

    def test_field_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        filter = fieldFilter.FieldFilter(self.first_course.subject)

        courses = self.university.filter_courses(filter)

        assert len(courses) == 1
        course = courses[0]
        assert course == self.first_course

    def test_free_elective_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        filter = freeElectiveFilter.FreeElectiveFilter()

        courses = self.university.filter_courses(filter)

        assert len(courses) == 2

    def test_and_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        sub_filter_1 = specificCourseFilter.SpecificCourseFilter(self.first_course)
        sub_filter_2 = specificCourseFilter.SpecificCourseFilter(self.second_course)

        filter = orFilter.OrFilter([sub_filter_1, sub_filter_2])

        courses = self.university.filter_courses(filter)

        assert len(courses) == 2

    def test_or_filter(self):
        self.h.insert_course(self.first_course)
        self.h.insert_course(self.second_course)

        sub_filter_1 = specificCourseFilter.SpecificCourseFilter(self.first_course)
        sub_filter_2 = specificCourseFilter.SpecificCourseFilter(self.second_course)

        filter = orFilter.OrFilter([sub_filter_1, sub_filter_2])

        courses = self.university.filter_courses(filter)

        assert len(courses) == 2

class TestUniversity_GetSimpleDegrees(TestUniversityWithDb):
    def test_no_degrees(self):
        degrees = self.university.get_simple_degrees()

        assert len(degrees) == 0

    def test_single_degree(self):
        input_degree = self.first_degree

        self.h.insert_degree(input_degree)

        degrees = self.university.get_simple_degrees()
        assert len(degrees) == 1
        degree = degrees[0]
        assert degree['id'] == str(input_degree.num_code)
        assert degree['name'] == input_degree.name

    def test_multiple_degrees(self):
        first_degree = self.first_degree

        self.h.insert_degree(first_degree)

        second_degree = self.second_degree
        self.h.insert_degree(second_degree)

        degrees = self.university.get_simple_degrees()
        assert len(degrees) == 2
        degrees.sort(key=lambda x: x['id'])
        first_result_degree, second_result_degree = degrees
        assert first_result_degree['id'] == str(first_degree.num_code)
        assert first_result_degree['name'] == first_degree.name

        assert second_result_degree['id'] == str(second_degree.num_code)
        assert second_result_degree['name'] == second_degree.name


# Not including exclusion or equivalent because that might be changed to individual courses rather
# than course requirements
