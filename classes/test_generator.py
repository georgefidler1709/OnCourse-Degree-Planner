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
import courseReq
import subjectReq
import course
import specificCourseFilter
import andFilter
import andReq
import minDegreeReq
import degree
import program
import term
import generator

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

# Make some degree requirements
# 1001 and 1002 and 1003
degree_req1001 = specificCourseFilter.SpecificCourseFilter(subj1001)
degree_req1002 = specificCourseFilter.SpecificCourseFilter(subj1002)
degree_req1003 = specificCourseFilter.SpecificCourseFilter(subj1003)
and_req = andFilter.AndFilter([degree_req1001, degree_req1002, degree_req1003])
degree_req = minDegreeReq.MinDegreeReq(and_req, 18)

degree1 = degree.Degree(1, "Bachelor of Testing", 2019, 2, [degree_req], 'BATE1')

gen = generator.Generator(degree1)
prog = gen.generate()

for enrollment in prog.courses:
    print("-----------------------")
    print(enrollment.course.name)
    print(enrollment.term.year, enrollment.term.term)

