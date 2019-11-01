"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_generator.py
Test the functions defined in generator.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from . import courseReq
from . import subjectReq
from . import course
from . import specificCourseFilter
from . import orFilter
from . import andReq
from . import minDegreeReq
from . import degree
from . import program
from . import term
from . import generator

t1 = term.Term(2019, 1)
t2 = term.Term(2019, 2)
t3 = term.Term(2019, 3)
t4 = term.Term(2020, 1)
t5 = term.Term(2020, 2)
t6 = term.Term(2020, 3)

# Make some courses
# subj1001
subj1001 = course.Course("SUBJ", 1001, "Subject1", 6, [t1, t2, t3, t4, t5, t6])

# subj1002, prereq subj1001
prereq1001 = subjectReq.SubjectReq(subj1001)
subj1002 = course.Course("SUBJ", 1002, "Subject2", 6, [t1, t3, t4, t6], prereq1001)

# subj1003, prereq subj1001 and 1002
prereq1002 = subjectReq.SubjectReq(subj1002)
req1001_and_1002 = andReq.AndReq([prereq1001, prereq1002])
subj1003 = course.Course("SUBJ", 1003, "Subject3", 6, [t1, t4], req1001_and_1002)


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

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1001, req1002, req1003], 'BAT1')

    gen = generator.Generator(degree1)
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

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1001, req1002, req1003])

    gen = generator.Generator(degree1)
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
    subj1005 = course.Course("SUBJ", 1005, "Subject5", 6, [t1, t3, t4, t6], prereq1001, prereq1002)

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1001, req1002, req1005])

    gen = generator.Generator(degree1)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1005)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1005) == t3


def test_exclusion():
    # make an exclusion subject
    subj1005 = course.Course("SUBJ", 1005, "Subject5", 6, [t1, t3, t4, t6], prereqs=prereq1001, exclusions=[subj1002])

    # Make some degree requirements
    # 1001 and 1002 and 1003
    filter1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)

    req1001 = minDegreeReq.MinDegreeReq(filter1001, 6)
    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1001, req1002, req1005])

    gen = generator.Generator(degree1)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert not prog.enrolled(subj1005)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3


def test_equivalent():
    # make an equivalent subject
    subj1005 = course.Course("SUBJ", 1005, "Subject5", 6, [t2, t3, t5, t6], equivalents=[subj1001])
    subj1001.add_equivalent(subj1005)

    # Make some degree requirements
    # 1002 requires 1001 but 1005 is an equivalent
    filter1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
    filter1005 = specificCourseFilter.SpecificCourseFilter(subj1005)

    req1002 = minDegreeReq.MinDegreeReq(filter1002, 6)
    req1005 = minDegreeReq.MinDegreeReq(filter1005, 6)

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1005, req1002])

    gen = generator.Generator(degree1)
    prog = gen.generate()

    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1005)
    assert not prog.enrolled(subj1001)

    assert prog.term_taken(subj1005) == t2
    assert prog.term_taken(subj1002) == t3


def test_term_cap_enrollment():
    # make a coreq subject
    subj1005 = course.Course("SUBJ", 1005, "Subject5", 6, [t1, t4])
    subj1006 = course.Course("SUBJ", 1006, "Subject6", 6, [t1, t2])
    subj1007 = course.Course("SUBJ", 1007, "Subject7", 6, [t1, t2])

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

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1001, req1005, req1006, req1007])

    gen = generator.Generator(degree1)
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

    degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [req1003, req1002, req1001])

    gen = generator.Generator(degree1)
    prog = gen.generate()

    assert prog.enrolled(subj1001)
    assert prog.enrolled(subj1002)
    assert prog.enrolled(subj1003)

    assert prog.term_taken(subj1001) == t1
    assert prog.term_taken(subj1002) == t3
    assert prog.term_taken(subj1003) == t4



test_single_course_requirements()
test_simple_or_requirement()
test_coreq()
test_exclusion()
test_equivalent()
test_term_cap_enrollment()
test_requirement_ordering()
