"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_freeElectiveFilter.py
Test the functions defined in freeElectiveFilter.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from classes import course
from classes import freeElectiveFilter
from classes import degree

f = freeElectiveFilter.FreeElectiveFilter()
deg = degree.Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty="Engineering", requirements=[], alpha_code='COMPA1')

def test_accepts_course():
    c = course.Course("SUBJ", '1001', "Subject1", 6, [], "SubjectFac")
    assert f.accepts_course(c, deg)
