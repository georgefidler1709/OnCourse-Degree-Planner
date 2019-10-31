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
from typing import Tuple

from classes import university

class DbQuerier:
    def __init__(self, db):
        self.db = db

    def query_db(self, query : str, args: Tuple = (), one = False) -> Tuple:
        # query function from flask documentation
        # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

        cur = self.db.execute(query, args)
        rv = cur.fetchall()
        return (rv[0] if rv else None) if one else rv


class TestUniversityWithDb():
    def setup_method(self, function):
        self.db = sqlite3.connect(":memory:", detect_types=sqlite3.PARSE_DECLTYPES)

        with open('../server/db/schema.sql') as f:
            self.db.executescript(f.read())

        with open('../server/db/setup_enums.sql') as f:
            self.db.executescript(f.read())

        self.querier = DbQuerier(self.db)

        self.university = university.University(self.querier.query_db)

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
        self.db.execute("insert into Degrees(name, code, id) values(?, ?, ?)", (name, code, id))

        year = 2019
        self.db.execute("insert into DegreeOfferings(year, degree_id) values(?, ?)", (year, id))

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert degree.name == name
        assert degree.year == year

    def test_single_degree_no_match(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        not_id = 55
        self.db.execute("insert into Degrees(name, code, id) values(?, ?, ?)", (name, code, id))

        year = 2019

        self.db.execute("insert into DegreeOfferings(year, degree_id) values(?, ?)", (year, id))


        degree = self.university.find_degree_number_code(not_id)

        assert degree is None

    def test_multiple_degrees(self):
        name = "TestDegree"
        code = "TestCode"
        id = 42
        self.db.execute("insert into Degrees(name, code, id) values(?, ?, ?)", (name, code, id))

        year = 2019
        self.db.execute("insert into DegreeOfferings(year, degree_id) values(?, ?)", (year, id))

        other_name = "OtherDegree"
        other_code = "OtherCode"
        other_id = 55
        self.db.execute("insert into Degrees(name, code, id) values(?, ?, ?)", (other_name,
            other_code, other_id))

        self.db.execute("insert into DegreeOfferings(year, degree_id) values(?, ?)", (year, other_id))

        degree = self.university.find_degree_number_code(id)

        assert degree is not None
        assert degree.name == name
        assert degree.year == year



