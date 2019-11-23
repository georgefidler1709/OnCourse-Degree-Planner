'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_dbGenerator.py
Test the functions defined in dbGenerator.py

'''

import pytest
import sqlite3

from typing import Tuple

from scraper import dbGenerator
from classes import course

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

    def store_db(self, command: str, args: Tuple = ()) -> int:
        # Store information in the database

        try:
            self.cursor.execute(command, args)

            insert_id = self.cursor.lastrowid
            self.db.commit()
        except sqlite3.IntegrityError as e:
            print(f'Failed integrity error with command \'{command}\' and args \'{args}\'')
            raise e

        return insert_id

    def get_requirements(self, course_id):
        return (self.get_prereqs(course_id), self.get_coreqs(course_id),
                self.get_exclusions(course_id), self.get_equivalents(course_id))

    def get_prereqs(self, course_id):
        prereq_id = self.get_prereq_id(course_id)

        if prereq_id is None:
            return None

        print(type(prereq_id))

        return self.query_db('''select * from CourseRequirements where id = ?''', (prereq_id, ),
                one=True)

    def get_coreqs(self, course_id):
        coreq_id = self.get_coreq_id(course_id)

        if coreq_id is None:
            return None

        return self.query_db('''select * from CourseRequirements where id = ?''', (coreq_id, ),
                one=True)

    def get_prereq_id(self, course_id):
        result = self.query_db('''select prereq from Courses where id = ?''', (course_id, ),
                one=True)

        if result is None:
            return None

        (prereq_id, ) = result
        return prereq_id

    def get_coreq_id(self, course_id):
        result = self.query_db('''select coreq from Courses where id = ?''', (course_id, ),
                one=True)

        if result is None:
            return None

        (coreq_id, ) = result
        return coreq_id

    def get_exclusions(self, course_id):
        exclusions = []

        results = self.query_db('''select first_course, second_course from ExcludedCourses where
        first_course = ? or second_course = ?''', (course_id, course_id))

        for result in results:
            first_course, second_course = result

            if first_course == course_id:
                exclusions.append(second_course)
            else:
                exclusions.append(first_course)

        return exclusions

    def get_equivalents(self, course_id):
        equivalents = []

        results = self.query_db('''select first_course, second_course from EquivalentCourses where
        first_course = ? or second_course = ?''', (course_id, course_id))

        for result in results:
            first_course, second_course = result

            if first_course == course_id:
                equivalents.append(second_course)
            else:
                equivalents.append(first_course)

        return equivalents


class TestDbGenerator():
    def setup_method(self, function):
        self.db = sqlite3.connect(':memory:', detect_types=sqlite3.PARSE_DECLTYPES)
        self.db.row_factory = sqlite3.Row

        self.cursor = self.db.cursor()

        with open('server/db/schema.sql') as f:
            self.db.executescript(f.read())

        with open('server/db/setup_enums.sql') as f:
            self.db.executescript(f.read())

        self.h = DbHelper(self.db)

        self.first_course = self.first_course = course.Course('TEST', '1000', 'Test course 1', 6, [], 'TestFaculty',
                finished=True)

        self.second_course = course.Course('COMP', '2521', 'Test course 2', 3, [], 'Engineering',
                finished=True)

        self.dbGenerator = dbGenerator.DbGenerator(self.h.query_db, self.h.store_db)



class TestDbGenerator_insert_requirements(TestDbGenerator):
    def setup_method(self, function):
        super().setup_method(function)

        self.first_course_id = self.dbGenerator.insert_course_without_requirements(self.first_course, 2020)
        self.second_course_id = self.dbGenerator.insert_course_without_requirements(self.second_course, 2020)

    def test_insert_nothing(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None, [], [])

        prereqs, coreqs, exclusions, equivalents = self.h.get_requirements(self.first_course_id)

        assert prereqs is None
        assert coreqs is None
        assert exclusions == []
        assert equivalents == []

    def test_insert_and_req(self):
        pass

    def test_insert_or_req(self):
        pass

    def test_insert_empty_uoc_req(self):
        pass

    def test_insert_wam_req(self):
        pass

    def test_insert_year_req(self):
        pass

    def test_insert_enrollment_req(self):
        pass

    def test_insert_subject_req(self):
        pass

    def test_insert_unparsed_req(self):
        pass

    def test_insert_exclusion(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None,
                [self.second_course.course_code], [])

        prereqs, coreqs, exclusions, equivalents = self.h.get_requirements(self.first_course_id)

        assert prereqs is None
        assert coreqs is None
        assert exclusions == [self.second_course_id]
        assert equivalents == []

    def test_insert_equivalent(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None,
                [], [self.second_course.course_code])

        prereqs, coreqs, exclusions, equivalents = self.h.get_requirements(self.first_course_id)

        assert prereqs is None
        assert coreqs is None
        assert exclusions == []
        assert equivalents == [self.second_course_id]


