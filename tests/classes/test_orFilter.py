"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_orFilter.py
Test the functions defined in orFilter.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from classes import course
from classes import orFilter
from classes import fieldFilter
from classes import levelFilter
from classes import degree



f1 = fieldFilter.FieldFilter("SUBJ")
f2 = fieldFilter.FieldFilter("OTHR")
deg = degree.Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty="Engineering", requirements=[], alpha_code='COMPA1')
c1 = course.Course("SUBJ", "1001", "Subject1", 6, [], "Engineering")
c2 = course.Course("FALS", "1001", "False1", 6, [], "Engineering")
or_filt1 = orFilter.OrFilter([f1, f2])

def test_accepts_course_true():
    assert or_filt1.accepts_course(c1, deg)

def test_accepts_course_false():
    assert not or_filt1.accepts_course(c2, deg)
