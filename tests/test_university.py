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

    def insert_degree(self, name="TestDegree", code="TestCode", id=42, year=2019, requirements=[]):
        self.cursor.execute("insert into Degrees(name, code, id) values(?, ?, ?)", (name, code, id))

        self.cursor.execute("insert into DegreeOfferings(year, degree_id) values(?, ?)", (year, id))

    def insert_course(self, letter_code="COMP", number_code="1511", level=1, name="Intro to computing", units=6):
        self.cursor.execute('''insert into Courses(letter_code, number_code, level, name, units) values
        (?, ?, ?, ?, ?)''', (letter_code, number_code, level, name,
        units))

        id = self.cursor.lastrowid
        return id

    def insert_degree_requirement(self, degree_id, year, filter_id, uoc_needed):
        self.cursor.execute('''insert into DegreeOfferingRequirements(offering_degree_id,
        offering_year_id, requirement_id, uoc_needed) values(?, ?, ?, ?)''', (degree_id, year, filter_id, uoc_needed))

class TestUniversityWithDb():
    def setup_method(self, function):
        self.db = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

        self.cursor = self.db.cursor()

        with open('server/db/schema.sql') as f:
            self.db.executescript(f.read())

        with open('server/db/setup_enums.sql') as f:
            self.db.executescript(f.read())

        self.h = DbHelper(self.db)

        self.university = university.University(self.h.query_db)

    def setup_teardown(self, function):
        self.db.close()

class TestUniversity_FindDegreeNumberCode(TestUniversityWithDb):
    def test_no_degrees(self):
        degree = self.university.find_degree_number_code(1)

        assert degree is None

    def test_single_degree(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id, year)
        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert len(degree.requirements) == 0
        assert degree.name == name
        assert degree.year == year

    def test_single_degree_no_match(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        not_id = 55
        self.h.insert_degree(name, code, id)

        degree = self.university.find_degree_number_code(not_id)

        assert degree is None

    def test_multiple_degrees(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42

        self.h.insert_degree(name, code, id)

        other_name = "OtherDegree"
        other_code = "OtherCode"
        other_id = 55

        self.h.insert_degree(other_name, other_code, other_id)
        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert degree.name == name

    def test_degree_with_specific_course_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        course_letter_code = "COMP"
        course_number_code = "1511"

        course_id = self.h.insert_course(course_letter_code, course_number_code)

        filter_type_id = self.h.get_filter_type_id("SpecificCourseFilter")
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
        assert filter.filter_name == "SpecificCourseFilter"
        course = filter.course
        assert course.subject == course_letter_code
        assert course.code == course_number_code

    def test_degree_with_gen_ed_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id("GenEdFilter")
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
        assert filter.filter_name == "GenEdFilter"

    def test_degree_with_field_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id("FieldFilter")
        field = "COMP"
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
        assert filter.filter_name == "FieldFilter"
        assert filter.field == field

    def test_degree_with_free_elective_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id("FreeElectiveFilter")

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
        assert filter.filter_name == "FreeElectiveFilter"


    def test_degree_with_and_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id("AndFilter")

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id("FreeElectiveFilter")

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
        assert filter.filter_name == "AndFilter"
        sub_filters = filter.filters
        assert len(sub_filters) == 1
        sub_filter = sub_filters[0]
        assert sub_filter.filter_name == "FreeElectiveFilter"

    def test_degree_with_or_filter(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        year = 2019

        self.h.insert_degree(name, code, id)

        filter_type_id = self.h.get_filter_type_id("OrFilter")

        self.cursor.execute('''insert into CourseFilters(type_id) values(?)''', (filter_type_id,))

        filter_id = self.cursor.lastrowid

        sub_filter_type_id = self.h.get_filter_type_id("FreeElectiveFilter")

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
        assert filter.filter_name == "OrFilter"
        sub_filters = filter.filters
        assert len(sub_filters) == 1
        sub_filter = sub_filters[0]
        assert sub_filter.filter_name == "FreeElectiveFilter"







