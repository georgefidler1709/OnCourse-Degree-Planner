'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_degree.py
Test the functions defined in degree.py

[MORE INFO ABOUT CLASS]
'''

import pytest

from classes.degree import Degree

@pytest.fixture
def compa1_shallow():
	deg = Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty='Engineering', requirements=[], alpha_code='COMPA1')
	return deg

def compa1_deep():
	

	deg = Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty='Engineering', requirements=[], alpha_code='COMPA1')


def test_url(compa1_shallow):
	url = compa1_shallow.get_url()

	assert url == 'https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778'


# faculty = 'SubjFaculty'
# t1 = term.Term(2019, 1)
# t2 = term.Term(2019, 2)
# degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 3, faculty, [], 'BAT1')
# subj1001 = course.Course('SUBJ', '1001', 'Subject1', 6, [t1, t2], faculty)
# subj1002 = course.Course('SUBJ', '1002', 'Subject1', 6, [t1, t2], faculty)
# enrol1001 = courseEnrollment.CourseEnrollment(subj1001, t1)
# enrol1002 = courseEnrollment.CourseEnrollment(subj1002, t1)
# prog1 = program.Program(degree1, [enrol1001], [])
# prog2 = program.Program(degree1, [enrol1002], [])
# req = subjectReq.SubjectReq(subj1001)

def test_get_requirements_no_requirements():
	deg = Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty='Engineering', requirements=[], alpha_code='COMPA1')
	assert len(deg.get_requirements()) == 0


def test_get_requirements_none_remaining():
	pass

def test_get_requirements_partial_free_remaining():
	pass

def test_get_requirements_partial_gen_remaining():
	pass

def test_get_requirements_partial_filt_remaining():
	pass

def test_get_requirements_partial_core_remaining():
	pass

def test_get_requirements_partial_all_remaining():
	pass

def test_get_requirements_all_remaining():
	pass

