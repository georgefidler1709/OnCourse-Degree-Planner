"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test file for CourseParser class
"""

import pytest
from . import courseParser
from . import scrapedSubjectReq
from . import scrapedEnrollmentReq
from classes import uocReq
from classes import yearReq
from classes import wamReq
from classes import orReq
from classes import andReq
from classes import fieldFilter
from classes import levelFilter
from classes import orFilter
from classes import andFilter

parser = courseParser.CourseParser()

def test_parse_terms():
    terms = parser.parse_terms("Term 1, Term 3", 2019)
    assert len(terms) == 2
    assert terms[0].year == 2019
    assert terms[0].term == 1
    assert terms[1].year == 2019
    assert terms[1].term == 3


def test_is_course_code():
    assert parser.is_course_code("COMP1511")
    assert not parser.is_course_code("COMP")
    assert not parser.is_course_code("12345678")


def test_split_by_conj_single_req():
    split, conj = parser.split_by_conj("COMP1511")
    assert len(split) == 1
    assert split[0] == "COMP1511"
    assert conj is None

def test_split_by_conj_one_level_no_brackets_and():
    split, conj = parser.split_by_conj("COMP1511 and uoc 48")
    assert len(split) == 2
    assert split[0] == "COMP1511"
    assert split[1] == "uoc 48"
    assert conj == "and"

def test_split_by_conj_one_level_no_brackets_or():
    split, conj = parser.split_by_conj("year 2 or uoc 48 l 3 f COMP")
    assert len(split) == 2
    assert split[0] == "year 2"
    assert split[1] == "uoc 48 l 3 f COMP"
    assert conj == "or"

def test_split_by_conj_one_level_brackets_and():
    split, conj = parser.split_by_conj("(enrol 3778 and uoc 48)")
    assert len(split) == 2
    assert split[0] == "enrol 3778"
    assert split[1] == "uoc 48"
    assert conj == "and"

def test_split_by_conj_one_level_brackets_or():
    split, conj = parser.split_by_conj("(COMP1521 or COMP1531)")
    assert len(split) == 2
    assert split[0] == "COMP1521"
    assert split[1] == "COMP1531"
    assert conj == "or"

def test_split_by_conj_two_levels_and_or():
    split, conj = parser.split_by_conj("(COMP1521 and COMP1531) or (enrol 3778 and uoc 48)")
    assert len(split) == 2
    assert split[0] == "(COMP1521 and COMP1531)"
    assert split[1] == "(enrol 3778 and uoc 48)"
    assert conj == "or"

def test_split_by_conj_two_levels_or_and():
    split, conj = parser.split_by_conj("(COMP1521 or COMP1531) and (enrol 3778 or uoc 48)")
    assert len(split) == 2
    assert split[0] == "(COMP1521 or COMP1531)"
    assert split[1] == "(enrol 3778 or uoc 48)"
    assert conj == "and"

def test_split_by_conj_complex():
    split, conj = parser.split_by_conj("(COMP1521 or DPST1092 or COMP2121) and (COMP1927 or COMP2521) and (uoc 75)")
    assert len(split) == 3
    assert split[0] == "(COMP1521 or DPST1092 or COMP2121)"
    assert split[1] == "(COMP1927 or COMP2521)"
    assert split[2] == "(uoc 75)"
    assert conj == "and"

def test_parse_uoc_req_filter_field():
    f = parser.parse_uoc_req_filter(["uoc","48", "f", "COMP"])
    assert isinstance(f, fieldFilter.FieldFilter)
    assert f.field == "COMP"

def test_parse_uoc_req_filter_fields():
    f = parser.parse_uoc_req_filter(["uoc","48", "f", "COMP", "SENG"])
    assert isinstance(f, orFilter.OrFilter)
    assert isinstance(f.filters[0], fieldFilter.FieldFilter)
    assert isinstance(f.filters[1], fieldFilter.FieldFilter)
    assert f.filters[0].field == "COMP"
    assert f.filters[1].field == "SENG"

def test_parse_uoc_req_filter_level():
    f = parser.parse_uoc_req_filter(["uoc","48", "l", "2"])
    assert isinstance(f, levelFilter.LevelFilter)
    assert f.level == 2

def test_parse_uoc_req_filter_levels():
    f = parser.parse_uoc_req_filter(["uoc","48", "l", "3", "4"])
    assert isinstance(f, orFilter.OrFilter)
    assert isinstance(f.filters[0], levelFilter.LevelFilter)
    assert isinstance(f.filters[1], levelFilter.LevelFilter)
    assert f.filters[0].level == 3
    assert f.filters[1].level == 4


def test_parse_uoc_req_filter_combination_f_l():
    f = parser.parse_uoc_req_filter(["uoc","48", "f", "COMP", "l", "3", "4"])
    assert isinstance(f, andFilter.AndFilter)
    assert isinstance(f.filters[0], fieldFilter.FieldFilter)
    assert isinstance(f.filters[1], orFilter.OrFilter)
    or_f = f.filters[1]
    assert or_f.filters[0].level == 3
    assert or_f.filters[1].level == 4

def test_parse_uoc_req_filter_combination_l_f():
    f = parser.parse_uoc_req_filter(["uoc","48", "l", "3", "4", "f", "COMP"])
    assert isinstance(f, andFilter.AndFilter)
    assert isinstance(f.filters[1], orFilter.OrFilter)
    assert isinstance(f.filters[0], fieldFilter.FieldFilter)
    or_f = f.filters[1]
    assert or_f.filters[0].level == 3
    assert or_f.filters[1].level == 4


# Make a single course req from a string
def test_make_single_course_req_subj():
    req = parser.make_single_course_req("COMP1511")
    assert isinstance(req, scrapedSubjectReq.ScrapedSubjectReq)
    assert req.course == "COMP1511"
    assert req.min_mark == 50

# Make a single course req with a min mark
def test_make_single_course_req_subj_mark():
    req = parser.make_single_course_req("COMP1511 75")
    assert isinstance(req, scrapedSubjectReq.ScrapedSubjectReq)
    assert req.course == "COMP1511"
    assert req.min_mark == 75

# Make a uoc requirement
def test_make_single_course_req_uoc():
    req = parser.make_single_course_req("uoc 48")
    assert isinstance(req, uocReq.UOCReq)
    assert req.uoc == 48

def test_make_single_course_req_uoc_filter():
    pass

def test_make_single_course_req_year():
    req = parser.make_single_course_req("year 2")
    assert isinstance(req, yearReq.YearReq)
    assert req.year == 2

def test_make_single_course_req_enrol():
    req = parser.make_single_course_req("enrol 3778")
    assert isinstance(req, scrapedEnrollmentReq.ScrapedEnrollmentReq)
    assert req.degree == 3778

def test_make_single_course_req_wam():
    req = parser.make_single_course_req("wam 75")
    assert isinstance(req, wamReq.WAMReq)
    assert req.wam == 75

def test_parse_course_req():
    req = parser.parse_course_req("(COMP1511 or DPST1092 or COMP2121) and (COMP1927 or COMP2521) and (wam 75)")
    assert isinstance(req, andReq.AndReq)
    assert isinstance(req.reqs[0], orReq.OrReq)
    assert isinstance(req.reqs[1], orReq.OrReq)
    assert isinstance(req.reqs[2], wamReq.WAMReq)
    or_1 = req.reqs[0]
    or_2 = req.reqs[1]
    assert len(or_1.reqs) == 3
    assert len(or_2.reqs) == 2
    assert isinstance(or_1.reqs[0], scrapedSubjectReq.ScrapedSubjectReq)
    assert or_1.reqs[0].course == "COMP1511"
    assert isinstance(or_1.reqs[1], scrapedSubjectReq.ScrapedSubjectReq)
    assert or_1.reqs[1].course == "DPST1092"
    assert isinstance(or_1.reqs[2], scrapedSubjectReq.ScrapedSubjectReq)
    assert or_1.reqs[2].course == "COMP2121"
    assert isinstance(or_2.reqs[0], scrapedSubjectReq.ScrapedSubjectReq)
    assert or_2.reqs[0].course == "COMP1927"
    assert isinstance(or_2.reqs[1], scrapedSubjectReq.ScrapedSubjectReq)
    assert or_2.reqs[1].course == "COMP2521"
    assert req.reqs[2].wam == 75

