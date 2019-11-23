'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_fieldFilter.py
Test the functions defined in fieldFilter.py
'''

import pytest
from classes import course
from classes import fieldFilter
from classes import degree

f = fieldFilter.FieldFilter('SUBJ')
deg = degree.Degree(num_code='3778', name='Computer Science', year=2019,
        duration=3, faculty='Engineering', requirements=[], alpha_code='COMPA1')

def test_accepts_course_true():
    c = course.Course('SUBJ', '1001', 'Subject1', 6, [], 'SubjectFac')
    assert f.accepts_course(c, deg)

def test_accepts_course_false():
    c = course.Course('OTHR', '1001', 'Other1', 6, [], 'OtherFac')
    assert not f.accepts_course(c, deg)
