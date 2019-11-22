'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_generator.py
Test the functions defined in generator.py

[MORE INFO ABOUT CLASS]
'''

import pytest
from typing import List, Optional

from classes import courseReq
from classes import subjectReq
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

# A simple mock university that just implements filter_courses, for the purpose of generator
# WARNING high dependency with University.filter_courses() function
# if you change University.filter_courses() you must change it here
class MockUniversity():
    def __init__(self):
        self.courses = []

    def add_course(self, course: 'course.Course') -> None:
        self.courses.append(course)

    def reset_courses(self, courses: List['course.Course']) -> None:
        self.courses = courses

    def filter_courses(self, desired_filter: 'courseFilter.CourseFilter', degree: 'degree.Degree', eq: bool=True) -> List['course.Course']:
        return list(filter(lambda x: desired_filter.accepts_course(x, degree, eq), self.courses))

    def find_course(self, code: str) -> Optional['course.Course']:
        for course in self.courses:
            if course.course_code == code:
                return course

        return None

uni = MockUniversity()


t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)
t3 = term.Term(2019, 3)
t4 = term.Term(2020, 1)
t5 = term.Term(2020, 2)
t6 = term.Term(2020, 3)

faculty = 'SubjFaculty'

# Make some courses
# subj1001
subj1001 = course.Course('SUBJ', '1001', 'Subject1', 6, [t1, t2, t3, t4, t5, t6], faculty)

# subj1002, prereq subj1001
prereq1001 = subjectReq.SubjectReq(subj1001)
subj1002 = course.Course('SUBJ', '1002', 'Subject2', 6, [t1, t3, t4, t6], faculty, prereq1001)

# subj1003, prereq subj1001 and 1002
prereq1002 = subjectReq.SubjectReq(subj1002)
req1001_and_1002 = andReq.AndReq([prereq1001, prereq1002])
subj1003 = course.Course('SUBJ', '1003', 'Subject3', 6, [t1, t4], faculty, req1001_and_1002)

# TODO subj1004 was not defined! making a dummy one
subj1004 = course.Course('SUBJ', '1004', 'Subject4', 6, [t1, t2], faculty, req1001_and_1002)

def setup_function(function):
    uni.reset_courses([subj1001, subj1002, subj1003, subj1004])


# test with simple chain of subjects with prerequisites
def test_single_course_requirements():
    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1002, req1003], 'BAT1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1003)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1003) == t4

# test with a choice between subjects
def test_simple_or_requirement():
    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
    filter1004 = specificCourseFilter.SpecificCourseFilter(subj1004)
    or_filter = orFilter.OrFilter([filter1002, filter1004])

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(or_filter, 6)
    req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1002, req1003], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1003)
    assert not prog.enrolled(subj1004)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1003) == t4

# check assignment with corequisite
def test_coreq():
    # make a coreq subject
    subj1005 = course.Course('SUBJ', '1005', 'Subject5', 6, [t1, t3, t4, t6], faculty, prereq1001, prereq1002)

    uni.add_course(subj1005)

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1002, req1005], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1005)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1005) == t3


def test_exclusion():
    # make an exclusion subject
    subj1005 = course.Course('SUBJ', '1005', 'Subject5', 6, [t1, t3, t4, t6], faculty,
            prereqs=prereq1001, exclusions=['SUBJ1002'])
    uni.add_course(subj1005)

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1002, req1005], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert not prog.enrolled(subj1005)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3


def test_equivalent():
    # make an equivalent subject
    subj1005 = course.Course('SUBJ', '1005', 'Subject5', 6, [], faculty, equivalents=['SUBJ1001'])
    subj1001.add_equivalent('SUBJ1005')

    subj1006 = course.Course('SUBJ', '1006', 'Subject5', 6, [t2, t3, t5, t6], faculty)

    uni.add_course(subj1005)
    uni.add_course(subj1006)

    # Make some degree requirements
    # 1006 requires 1005 but 1001 is an equivalent
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)
    filter1006 = specificCourseFilter.SpecificCourseFilter(subj1006)

    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)
    req1006 = minDegreeReq.MinDegreeReq(filter1006, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1005, req1006], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1006)
    assert not prog.enrolled(subj1005)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1006) == t2


def test_term_cap_enrollment():
    # make a coreq subject
    subj1005 = course.Course('SUBJ', '1005', 'Subject5', 6, [t1, t4], faculty)
    subj1006 = course.Course('SUBJ', '1006', 'Subject6', 6, [t1, t2], faculty)
    subj1007 = course.Course('SUBJ', '1007', 'Subject7', 6, [t1, t2], faculty)

    uni.add_course(subj1005)
    uni.add_course(subj1006)
    uni.add_course(subj1007)

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)
    filter1006 = specificCourseFilter.SpecificCourseFilter(subj1006)
    filter1007 = specificCourseFilter.SpecificCourseFilter(subj1007)

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)
    req1006 = minDegreeReq.MinDegreeReq(filter1006, 6)
    req1007 = minDegreeReq.MinDegreeReq(filter1007, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1005, req1006, req1007], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1005)
    assert prog.enrolled(subj1006)
    assert prog.enrolled(subj1007)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1005) == t1
    assert prog.term_taken(subj1006) == t1
    assert prog.term_taken(subj1007) == t2

# test that enrollments work even if requirements given against prerequisite order
def test_requirement_ordering():
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1003, req1002, req1001], 'TESTA1')

    gen = generator.Generator(degree1, uni)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1003)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1003) == t4

def test_prior_studies_simple():
    prior = [subj1001, subj1002]

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1003 = minDegreeReq.MinDegreeReq(filter1003, 6)

    degree1 = degree.Degree(1, 'Bachelor of Testing', 2019, 2, faculty, [req1001, req1002, req1003], 'BAT1')

    gen = generator.Generator(degree1, uni, prior)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1003)

    assert prog.term_taken(subj1003) == t1
    assert prog.term_taken(subj1001) == None
    assert prog.term_taken(subj1002) == None

    assert prog.unit_count_total() == 18
    assert degree1.complete(prog)
