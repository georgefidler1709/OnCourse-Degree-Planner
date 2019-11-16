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
from classes import orReq
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
from classes import courseEnrollment


t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)

faculty = "SubjFaculty"

degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 3, faculty, [], 'BAT1')

def test_eq():
    subj1001 = course.Course("SUBJ", 1001, "Subject1", 6, [t1, t2], faculty)
    subj1001_2 = course.Course("SUBJ", 1001, "Subject1", 6, [t1, t2], faculty)
    subj1002 = course.Course("SUBJ", 1002, "Subject2", 6, [t1, t2], faculty)

    assert subj1001 == subj1001
    assert subj1001 == subj1001_2
    assert subj1001_2 == subj1001
    assert not subj1002 == subj1001
    assert not subj1001 == subj1002


def test_check_reqs():

    subj1001 = course.Course("SUBJ", 1001, "Subject1", 6, [t1, t2], faculty)
    subj1002 = course.Course("SUBJ", 1002, "Subject2", 6, [t1, t2], faculty)
    subj1003 = course.Course("SUBJ", 1003, "Subject3", 6, [t1, t2], faculty)
    subj1004 = course.Course("SUBJ", 1004, "Subject4", 6, [t1, t2], faculty)
    subj1005 = course.Course("SUBJ", 1005, "Subject5", 6, [t1, t2], faculty)
    subj1006 = course.Course("SUBJ", 1006, "Subject6", 6, [t1, t2], faculty)

    req1001 = subjectReq.SubjectReq(subj1001, 75)
    req1002 = subjectReq.SubjectReq(subj1002)
    req1003 = subjectReq.SubjectReq(subj1003)
    req1004 = subjectReq.SubjectReq(subj1004)

    req1002_and = andReq.AndReq([req1002, req1003])
    prereq_or = orReq.OrReq([req1001, req1002_and])

    ex = [subj1005, subj1006]
    subj1007 = course.Course("SUBJ", 1007, "Subject7", 6, [t1, t2], faculty,
                        prereqs=prereq_or, coreqs=req1004, exclusions=ex)

    
    enrol1005 = courseEnrollment.CourseEnrollment(subj1005, t1)

    prog = program.Program(degree1, [enrol1005])

    errors = subj1007.check_reqs(prog, t2)

    assert len(errors) == 3
    assert errors[0][0] == "Prerequisite:"
    assert errors[0][1] == ["(A mark of 75 in SUBJ1001 OR (SUBJ1002 AND SUBJ1003))"]
    assert errors[1][0] == "Corequisite:"
    assert errors[1][1] == ["SUBJ1004"]
    assert errors[2][0] == "Exclusion:"
    assert errors[2][1] == ["SUBJ1005"]

    prog.add_course(subj1001, t1)
    errors = subj1007.check_reqs(prog, t2)
    assert len(errors) == 2
    assert errors[0][0] == "Corequisite:"
    assert errors[0][1] == ["SUBJ1004"]
    assert errors[1][0] == "Exclusion:"
    assert errors[1][1] == ["SUBJ1005"]

    assert subj1007.check_warnings(prog, t2) == ["A mark of 75 in SUBJ1001"]

    

