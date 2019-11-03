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

from classes import university

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

    def insert_degree(self, name='TestDegree', code='TestCode', id=42, year=2019, requirements=[]):
        self.cursor.execute('insert into Degrees(name, code, id) values(?, ?, ?)', (name, code, id))

        self.cursor.execute('insert into DegreeOfferings(year, degree_id) values(?, ?)', (year, id))

    def insert_course(self, letter_code='COMP', number_code='1511', level=1,
            name='Intro to computing', units=6, prereq=None, coreq=None, exclusion=None,
            equivalent=None):
        self.cursor.execute('''insert into Courses(letter_code, number_code, level, name, units,
        prereq, coreq, exclusion, equivalent) values (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (letter_code, number_code, level, name, units, prereq, coreq, exclusion, equivalent))

        id = self.cursor.lastrowid
        return id

    def insert_degree_requirement(self, degree_id, year, filter_id, uoc_needed):
        self.cursor.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
        offering_year_id, requirement_id, uoc_needed) values(?, ?, ?, ?)''', (degree_id, year, filter_id, uoc_needed))

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

    def teardown_method(self, function):
        self.db.close()

class TestUniversity_FindDegreeNumberCode(TestUniversityWithDb):
    def test_no_degrees(self):
        degree = self.university.find_degree_number_code(1)

        assert degree is None

    def test_single_degree(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id, year)
        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 0
        assert degree.name == name
        assert degree.year == year

    def test_single_degree_no_match(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        not_id = 55
        self.h.insert_degree(name, code, id)

        degree = self.university.find_degree_number_code(not_id)

        assert degree is None

    def test_multiple_degrees(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42

        self.h.insert_degree(name, code, id)

        other_name = 'OtherDegree'
        other_code = 'OtherCode'
        other_id = 55

        self.h.insert_degree(other_name, other_code, other_id)
        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert degree.name == name

    def test_degree_with_specific_course_filter(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        course_letter_code = 'COMP'
        course_number_code = '1511'

        course_id = self.h.insert_course(course_letter_code, course_number_code)

        filter_type_id = self.h.get_filter_type_id('SpecificCourseFilter')
        print(filter_type_id)

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id, min_mark, course_id) values(?, ?,
        ?)''', (filter_type_id, mark_needed, course_id))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'SpecificCourseFilter'
        course = filter.course
        assert course.subject == course_letter_code
        assert course.code == course_number_code

    def test_degree_with_gen_ed_filter(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id('GenEdFilter')
        print(filter_type_id)

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'GenEdFilter'

    def test_degree_with_field_filter(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id('FieldFilter')
        field = 'COMP'
        level = 2

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id, field_code, level) values(?, ?,
                ?)''', (filter_type_id, field, level))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'FieldFilter'
        assert filter.field == field

    def test_degree_with_free_elective_filter(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        mark_needed = 90

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 1
        requirement = degree.requirements[0]
        assert requirement.uoc == uoc_needed
        filter = requirement.filter
        assert filter.filter_name == 'FreeElectiveFilter'


    def test_degree_with_and_filter(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id('AndFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (sub_filter_type_id, ))

        sub_filter_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseFilterHierarchies(parent_id, child_id) values(?,
        ?)''', (filter_id, sub_filter_id))


        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

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
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id('OrFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id('FreeElectiveFilter')

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (sub_filter_type_id, ))

        sub_filter_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseFilterHierarchies(parent_id, child_id) values(?,
        ?)''', (filter_id, sub_filter_id))


        uoc_needed = 51

        self.h.insert_degree_requirement(id, year, filter_id, uoc_needed)

        degree = self.university.find_degree_number_code(id)

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
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 12

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name, units)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        assert course.subject == course_letter_code
        assert course.code == course_number_code
        assert course.name == course_name
        assert course.units == units

    def test_multiple_courses(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name, units)

        other_course_letter_code = 'FAKE'
        other_course_number_code = '3235'
        other_course_level = 2
        other_course_name = 'Other Test course'
        other_units = 3

        self.h.insert_course(other_course_letter_code, other_course_number_code, other_course_level, other_course_name, other_units)


        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        assert course.subject == course_letter_code
        assert course.code == course_number_code
        assert course.name == course_name
        assert course.units == units

    def test_course_with_completed_course_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        other_course_letter_code = 'COMP'
        other_course_number_code = '1511'
        other_course_level = 2
        other_course_name = 'Other course'
        other_course_units = 3

        other_course_id = self.h.insert_course(other_course_letter_code, other_course_number_code,
                other_course_level, other_course_name, other_course_units)


        type_id = self.h.get_requirement_type_id('CompletedCourseRequirement')
        min_mark = 75

        self.cursor.execute('''insert into CourseRequirements(type_id, min_mark, course_id)
        values(?, ?, ?)''', (type_id, min_mark, other_course_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CompletedCourseRequirement'
        required_course = prereq.course
        assert required_course.subject == other_course_letter_code
        assert required_course.code == other_course_number_code

    def test_course_with_degree_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        degree_name = 'TestDegree'
        degree_code = 'TestCode'
        degree_id = 42
        degree_year = 2019

        self.h.insert_degree(degree_name, degree_code, degree_id, degree_year)

        type_id = self.h.get_requirement_type_id('CurrentDegreeRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, degree_id) values(?, ?)''',
                (type_id, degree_id))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CurrentDegreeRequirement'
        required_degree = prereq.degree
        assert required_degree is not None
        assert required_degree.num_code == degree_id
        assert required_degree.name == degree_name

    def test_course_with_year_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        year = 2

        type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, year))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == year

    def test_course_with_uoc_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

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

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'UocRequirement'
        assert prereq.uoc == requirement_uoc_required
        filter = prereq.filter
        assert filter.filter_name == 'FieldFilter'

    def test_course_with_and_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

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

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'AndRequirement'
        sub_requirements = prereq.reqs
        assert len(sub_requirements) == 1
        sub_requirement = sub_requirements[0]
        assert sub_requirement.requirement_name == 'YearRequirement'

    def test_course_with_or_prereq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        year = 2

        sub_requirement_type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (sub_requirement_type_id, year))

        sub_requirement_id = self.cursor.lastrowid

        requirement_type_id =  self.h.get_requirement_type_id('OrRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id) values(?)''',
                (requirement_type_id,))

        requirement_id = self.cursor.lastrowid

        self.cursor.execute('''insert into CourseRequirementHierarchies(parent_id, child_id)
        values(?, ?)''', (requirement_id, sub_requirement_id))

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'OrRequirement'
        sub_requirements = prereq.reqs
        assert len(sub_requirements) == 1
        sub_requirement = sub_requirements[0]
        assert sub_requirement.requirement_name == 'YearRequirement'

    def test_course_with_coreq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
        units = 50

        year = 2

        type_id = self.h.get_requirement_type_id('YearRequirement')

        self.cursor.execute('''insert into CourseRequirements(type_id, year) values(?, ?)''',
                (type_id, year))

        requirement_id = self.cursor.lastrowid

        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, coreq=requirement_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None
        assert course.prereqs is None
        coreq = course.coreqs
        assert coreq is not None
        assert coreq.requirement_name == 'YearRequirement'
        assert coreq.year == year

    def test_course_with_prereq_and_coreq(self):
        course_letter_code = 'TEST'
        course_number_code = '4999'
        course_level = 3
        course_name = 'Test course'
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



        self.h.insert_course(course_letter_code, course_number_code, course_level, course_name,
                units, prereq=prereq_id, coreq=coreq_id)

        course = self.university.find_course(course_letter_code + course_number_code)

        assert course is not None

        coreq = course.coreqs
        assert coreq is not None
        assert coreq.requirement_name == 'YearRequirement'
        assert coreq.year == coreq_year

        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == prereq_year

class TestUniversity_GetSimpleDegrees(TestUniversityWithDb):
    def test_no_degrees(self):
        degrees = self.university.get_simple_degrees()

        assert len(degrees) == 0

    def test_single_degree(self):
        name = 'TestDegree'
        code = 'TestCode'
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id, year)

        degrees = self.university.get_simple_degrees()
        assert len(degrees) == 1
        degree = degrees[0]
        assert degree['id'] == code # TODO: I think this should use id instead, as code is just for
        # majors id
        assert degree['name'] == name

    def test_multiple_degrees(self):
        first_name = 'TestDegree1'
        first_code = 'TestCode1'
        first_id = 42
        first_year = 2019

        self.h.insert_degree(first_name, first_code, first_id, first_year)

        second_name = 'TestDegree2'
        second_code = 'TestCode2'
        second_id = 60
        second_year = 2018

        self.h.insert_degree(second_name, second_code, second_id, second_year)

        degrees = self.university.get_simple_degrees()
        assert len(degrees) == 2
        degrees.sort(key=lambda x: x['id'])
        first_degree, second_degree = degrees
        assert first_degree['id'] == first_code # TODO: As above with code<->id
        assert first_degree['name'] == first_name

        assert second_degree['id'] == second_code # TODO: As above
        assert second_degree['name'] == second_name


# Not including exclusion or equivalent because that might be changed to individual courses rather
# than course requirements
