"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_yearReq.py
Test the functions defined in yearReq.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from typing import List

from classes import courseReq
from classes import subjectReq
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
from classes import courseEnrollment

# A simple mock university that just implements filter_courses, for the purpose of generator
class MockUniversity():
    def __init__(self):
        self.courses = []

    def add_course(self, course: 'course.Course') -> None:
        self.courses.append(course)

    def reset_courses(self, courses: List['course.Course']) -> None:
        self.courses = courses

    def filter_courses(self, desired_filter: 'courseFilter.CourseFilter', degree: 'degree.Degree', eq: bool=False) -> List['course.Course']:
        return list(filter(lambda x: desired_filter.accepts_course(x, degree, eq), self.courses))

uni = MockUniversity()

t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)
t3 = term.Term(2019, 3)
t4 = term.Term(2020, 1)
t5 = term.Term(2020, 2)
t6 = term.Term(2020, 3)
t7 = term.Term(2021, 1)
t8 = term.Term(2021, 2)
t9 = term.Term(2021, 3)

faculty = "SubjFaculty"

def test_one():
	# Make some courses
	# subj1001
	subj1001 = course.Course("SUBJ", '1001', "Subject1", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty)

	# subj1002, prereq subj1001
	prereq1001 = subjectReq.SubjectReq(subj1001)
	prereq_year2 = yearReq.YearReq(year=2)
	assert prereq_year2.year == 2
	req1001_and_year2 = andReq.AndReq([prereq1001, prereq_year2])
	subj1002 = course.Course("SUBJ", '1002', "Subject2", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty, req1001_and_year2)

	# subj1003, prereq subj1001 and 1002
	prereq_final = yearReq.YearReq(year=-1)
	assert prereq_final.year == -1
	req1001_and_final = andReq.AndReq([prereq1001, prereq_final])
	subj1003 = course.Course("SUBJ", '1003', "Subject3", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty, req1001_and_final)

	uni.reset_courses([subj1001, subj1002, subj1003])


	filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
	filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
	filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
	req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
	req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
	req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

	degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 3, faculty, [req1001, req1002, req1003], 'BAT1')

	gen = generator.Generator(degree1, uni)
	prog = gen.generate()

	assert prog.enrolled(subj1001)
	assert prog.enrolled(subj1002)
	assert prog.enrolled(subj1003)

	assert prog.term_taken(subj1001) == t1
	assert prog.term_taken(subj1002) == t4
	assert prog.term_taken(subj1003) == t7

def test_check():
	# Make some courses
	# subj1001
	subj1001 = course.Course("SUBJ", '1001', "Subject1", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty)

	# subj1002, prereq subj1001
	prereq1001 = subjectReq.SubjectReq(subj1001)
	subj1002 = course.Course("SUBJ", '1002', "Subject2", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty, prereq1001)

	# subj1003, prereq subj1001 and 1002
	subj1003 = course.Course("SUBJ", '1003', "Subject3", 6, [t1, t2, t3, t4, t5, t6, t7, t8, t9], faculty, prereq1001)

	uni.reset_courses([subj1001, subj1002, subj1003])

	filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
	filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
	filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
	req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
	req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
	req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)
	degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, faculty, [req1001, req1002, req1003], 'BAT1')

	enrol1001 = courseEnrollment.CourseEnrollment(subj1001, t1)
	enrol1002 = courseEnrollment.CourseEnrollment(subj1002, t2)
	enrol1003 = courseEnrollment.CourseEnrollment(subj1003, t7)

	prog = program.Program(degree1, [enrol1001, enrol1002, enrol1003], [])

	req = yearReq.YearReq(2)
	assert len(req.check(prog, t1)) == 1
	assert len(req.check(prog, t2)) == 1
	assert len(req.check(prog, t3)) == 1
	assert len(req.check(prog, t4)) == 0
	assert len(req.check(prog, t5)) == 0
	assert len(req.check(prog, t6)) == 0
	assert len(req.check(prog, t7)) == 0
	assert len(req.check(prog, t8)) == 0
	assert len(req.check(prog, t9)) == 0
	assert req.check(prog, t3)[0] == "Year 2 in your degree"

	req = yearReq.YearReq(-1)
	assert len(req.check(prog, t1)) == 1
	assert len(req.check(prog, t2)) == 1
	assert len(req.check(prog, t3)) == 1
	assert len(req.check(prog, t4)) == 1
	assert len(req.check(prog, t5)) == 1
	assert len(req.check(prog, t6)) == 1
	assert len(req.check(prog, t7)) == 0
	assert len(req.check(prog, t8)) == 0
	assert len(req.check(prog, t9)) == 0
	assert req.check(prog, t3)[0] == "Final year in your degree"

