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
from scraper import scrapedEnrollmentReq
from scraper import scrapedSubjectReq

from classes import (
        andFilter,
        andReq,
        course,
        enrollmentReq,
        fieldFilter,
        freeElectiveFilter,
        genEdFilter,
        levelFilter,
        orFilter,
        orReq,
        specificCourseFilter,
        subjectReq,
        university,
        unparsedReq,
        uocReq,
        wamReq,
        yearReq,
        )

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

        self.first_degree_id = 42
        self.first_degree_name = 'Test degree'
        self.first_degree_faculty = 'Faculty of Testing'
        self.first_degree_duration = 3

        self.h.store_db('''insert into Degrees(name, faculty, duration, id) values(?, ?, ?, ?)''',
                (self.first_degree_name, self.first_degree_faculty,
                    self.first_degree_duration, self.first_degree_id))

        self.uni = university.University(self.h.query_db)

    def test_insert_nothing(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)

        assert course.prereqs is None
        assert course.coreqs is None
        assert course.exclusions == []
        assert course.equivalents == []

    def test_insert_and_req(self):
        wam = 40
        sub_requirement = wamReq.WAMReq(wam)

        requirement = andReq.AndReq([sub_requirement])

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'AndRequirement'
        assert len(prereq.reqs) == 1
        sub_req = prereq.reqs[0]
        assert sub_req.requirement_name == 'WamRequirement'
        assert sub_req.wam == wam

    def test_insert_or_req(self):
        wam = 40
        sub_requirement = wamReq.WAMReq(wam)

        requirement = orReq.OrReq([sub_requirement])

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'OrRequirement'
        assert len(prereq.reqs) == 1
        sub_req = prereq.reqs[0]
        assert sub_req.requirement_name == 'WamRequirement'
        assert sub_req.wam == wam

    def test_insert_empty_uoc_req(self):
        uoc = 20
        requirement = uocReq.UOCReq(uoc, None)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'UocRequirement'
        assert prereq.uoc == uoc
        assert prereq.filter is None

    def test_insert_wam_req(self):
        wam = 40
        requirement = wamReq.WAMReq(wam)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'WamRequirement'
        assert prereq.wam == wam

    def test_insert_year_req(self):
        year = 3
        requirement = yearReq.YearReq(year)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'YearRequirement'
        assert prereq.year == year

    def test_insert_enrollment_req(self):
        requirement = scrapedEnrollmentReq.ScrapedEnrollmentReq(self.first_degree_id)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CurrentDegreeRequirement'
        assert prereq.degree_id == self.first_degree_id
        assert prereq.degree_name == self.first_degree_name


    def test_insert_subject_req(self):
        min_mark = 75
        requirement = scrapedSubjectReq.ScrapedSubjectReq(self.second_course.course_code, min_mark)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'CompletedCourseRequirement'
        assert prereq.course == self.second_course
        assert prereq.min_mark == min_mark

    def test_insert_unparsed_req(self):
        requirement_string = 'This is an unparsed requirement'

        requirement = unparsedReq.UnparsedReq(requirement_string)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'UnparsedRequirement'
        assert prereq.requirement_string == requirement_string

    def test_insert_prereq(self):
        requirement_string = 'This is an unparsed requirement'

        requirement = unparsedReq.UnparsedReq(requirement_string)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.requirement_name == 'UnparsedRequirement'
        assert prereq.requirement_string == requirement_string
        assert course.coreqs is None
        assert course.exclusions == []
        assert course.equivalents == []

    def test_insert_coreq(self):
        requirement_string = 'This is an unparsed requirement'

        requirement = unparsedReq.UnparsedReq(requirement_string)

        self.dbGenerator.insert_requirements(self.first_course_id, None, requirement, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        coreq = course.coreqs
        assert coreq is not None
        assert coreq.requirement_name == 'UnparsedRequirement'
        assert coreq.requirement_string == requirement_string
        assert course.prereqs is None
        assert course.exclusions == []
        assert course.equivalents == []

    def test_insert_exclusion(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None,
                [self.second_course.course_code], [])

        course = self.uni.find_course(self.first_course.course_code)

        assert course.prereqs is None
        assert course.coreqs is None
        assert course.exclusions == [self.second_course.course_code]
        assert course.equivalents == []


    def test_insert_equivalent(self):
        self.dbGenerator.insert_requirements(self.first_course_id, None, None,
                [], [self.second_course.course_code])

        course = self.uni.find_course(self.first_course.course_code)

        assert course.prereqs is None
        assert course.coreqs is None
        assert course.exclusions == []
        assert course.equivalents == [self.second_course.course_code]

    def test_insert_uoc_req_with_and_filter(self):
        input_sub_filter = freeElectiveFilter.FreeElectiveFilter()

        input_filter = andFilter.AndFilter([input_sub_filter])

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name
        assert len(filter.filters) == 1
        sub_filter = filter.filters[0]
        assert sub_filter.filter_name == input_sub_filter.filter_name
        
    def test_insert_uoc_req_with_or_filter(self):
        input_sub_filter = freeElectiveFilter.FreeElectiveFilter()

        input_filter = orFilter.OrFilter([input_sub_filter])

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name
        assert len(filter.filters) == 1
        sub_filter = filter.filters[0]
        assert sub_filter.filter_name == input_sub_filter.filter_name

    def test_insert_uoc_req_with_field_filter(self):
        field = 'COMP'
        input_filter = fieldFilter.FieldFilter(field)

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name
        assert filter.field == field

    def test_insert_uoc_req_with_free_elective_filter(self):
        input_filter = freeElectiveFilter.FreeElectiveFilter()

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name

    def test_insert_uoc_req_with_gen_ed_filter(self):
        input_filter = genEdFilter.GenEdFilter()

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name

    def test_insert_uoc_req_with_level_filter(self):
        level = 3
        input_filter = levelFilter.LevelFilter(level)

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name
        assert filter.level == input_filter.level

    def test_insert_uoc_req_with_specific_course_filter(self):
        input_filter = specificCourseFilter.SpecificCourseFilter(self.second_course)

        uoc = 20
        requirement = uocReq.UOCReq(uoc, input_filter)

        self.dbGenerator.insert_requirements(self.first_course_id, requirement, None, [], [])

        course = self.uni.find_course(self.first_course.course_code)
        prereq = course.prereqs
        assert prereq is not None
        assert prereq.filter is not None
        filter = prereq.filter
        assert filter.filter_name == input_filter.filter_name
        assert filter.course == input_filter.course












