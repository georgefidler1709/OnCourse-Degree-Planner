'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_andFilter.py
Test the functions defined in andFilter.py
'''

import pytest
from classes import course
from classes import andFilter
from classes import fieldFilter
from classes import levelFilter
from classes import degree


f = fieldFilter.FieldFilter('SUBJ')
l = levelFilter.LevelFilter(3)
deg = degree.Degree(num_code='3778', name='Computer Science', year=2019,
        duration=3, faculty='Engineering', requirements=[], alpha_code='COMPA1')
c1 = course.Course('SUBJ', '3001', 'Subject1', 6, [], 'Engineering')
c2 = course.Course('SUBJ', '1001', 'Subject1', 6, [], 'Engineering')
and_filt = andFilter.AndFilter([f, l])


def test_accepts_course_true():
    assert and_filt.accepts_course(c1, deg)

def test_accepts_course_false():
    assert not and_filt.accepts_course(c2, deg)
