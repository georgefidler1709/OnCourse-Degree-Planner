"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_course.py
Test the functions defined in course.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from typing import List

from classes import courseReq
from classes import subjectReq
from classes import uocReq
from classes import yearReq
from classes import course
from classes import courseFilter
from classes import specificCourseFilter
from classes import orFilter
from classes import andReq
from classes import minDegreeReq
from classes import degree
from classes import program
from classes import term
from classes import generator


t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)

faculty = "SubjFaculty"

# subj1001
subj1001 = course.Course("SUBJ", 1001, "Subject1", 6, [t1, t2], faculty)

# subj1003, prereq subj1001 and final year
prereq_final = yearReq.YearReq(year=-1)
prereq1001 = subjectReq.SubjectReq(subj1001)

req1001_and_final = andReq.AndReq([prereq1001, prereq_final])
subj1003 = course.Course("SUBJ", 1003, "Subject3", 6, [t1, t2], faculty, req1001_and_final)

subj1004 = course.Course("SUBJ", 1004, "Subject4", 6, [t1, t2], faculty)

filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
filter1004 = specificCourseFilter.SpecificCourseFilter(subj1004)

# subj1002, prereq 6 uoc from subj1003, 1004
or_filter = orFilter.OrFilter([filter1003, filter1004])
prereq_6uoc = uocReq.UOCReq(6, or_filter)
assert prereq_6uoc.filter is not None
subj1002 = course.Course("SUBJ", 1002, "Subject2", 6, [t1, t2], faculty, prereq_6uoc)

filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)

req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 3, faculty, [req1001, req1002, req1003], 'BAT1')


def test_check_reqs():
    prog = program.Program(degree1, [])
    assert len(subj1001.check_reqs(prog, t1)) == 0
    assert len(subj1002.check_reqs(prog, t1)) == 1
    assert subj1002.check_reqs(prog, t1)[0][0] == "Prerequisite:"
    assert subj1002.check_reqs(prog, t1)[0][1] == ["6 UoC fulfilling [(SUBJ1003) OR (SUBJ1004)]"]