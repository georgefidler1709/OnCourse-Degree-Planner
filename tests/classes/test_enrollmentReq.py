'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_enrollmentReq.py
Test the functions defined in enrollmentReq.py
'''

import pytest
from typing import List

from classes import degree
from classes import program
from classes import term
from classes import enrollmentReq


faculty = 'SubjFaculty'
t1 = term.Term(2019, 1)
degree1 = degree.Degree('1', 'Bachelor of Testing', 2019, 3, faculty, [], 'BAT1')
degree2 = degree.Degree('2', 'Bachelor of Testing2', 2019, 3, faculty, [], 'BAT2')
prog1 = program.Program(degree1, [], [])
prog2 = program.Program(degree2, [], [])
req = enrollmentReq.EnrollmentReq(degree1.num_code, degree1.name)

def test_fulfilled():
    assert req.fulfilled(prog1, t1)


def test_not_fulfilled():
    assert not req.fulfilled(prog2, t1)

def test_check():
    assert len(req.check(prog1, t1)) == 0
    assert len(req.check(prog2, t1)) == 1
    assert req.check(prog2, t1)[0] == 'Enrollment in Bachelor of Testing (1)'

