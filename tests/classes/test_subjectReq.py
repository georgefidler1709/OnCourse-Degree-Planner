"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_subjectReq.py
Test the functions defined in subjectReq.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from typing import List

from classes import degree
from classes import program
from classes import term
from classes import subjectReq
from classes import course
from classes import courseEnrollment


faculty = "SubjFaculty"
t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)
degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 3, faculty, [], 'BAT1')
subj1001 = course.Course("SUBJ", 1001, "Subject1", 6, [t1], faculty)
subj1002 = course.Course("SUBJ", 1002, "Subject1", 6, [t1], faculty)
enrol1001 = courseEnrollment.CourseEnrollment(subj1001, t1)
enrol1002 = courseEnrollment.CourseEnrollment(subj1002, t1)
prog1 = program.Program(degree1, [enrol1001])
prog2 = program.Program(degree1, [enrol1002])
req = subjectReq.SubjectReq(subj1001)

def test_fulfilled():
    assert req.fulfilled(prog1, t2)
    assert req.fulfilled(prog1, t1, coreq=True)


def test_not_fulfilled():
    assert not req.fulfilled(prog2, t2)


def test_check():
    assert len(req.check(prog1, t2)) == 0
    assert len(req.check(prog1, t1)) == 1
    assert len(req.check(prog2, t2)) == 1
    assert req.check(prog2, t2)[0] == "SUBJ1001"