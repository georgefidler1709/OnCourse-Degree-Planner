# IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE frontend/src/Api.tsx TO MATCH
'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

apiTypes.py
Contains the json layout of the types to be sent over to the front end
'''

import json
from typing import List, Dict
from mypy_extensions import TypedDict

class SimpleDegree(TypedDict):
    id: str;
    years: List[str];
    name: str;

class SimpleDegrees(TypedDict):
    degrees: List[SimpleDegree]
    years: List[str]

class SimpleCourse(TypedDict):
    id: str;
    name: str;

SimpleCourses = List[SimpleCourse]

class TermPlan(TypedDict):
    course_ids: List[str];
    term: int;

class YearPlan(TypedDict):
    term_plans: List[TermPlan];
    year: int;

class RemainReq(TypedDict):
    units: int;
    filter_type: str;
    # list of conditions / courses
    info: str;

class Program(TypedDict):
    # Degree object
    id: str;
    name: str;
    year: int;
    duration: int; # in years
    url: str; # degree handbook url
    notes: List[str];

    # List of CourseEnrollments
    enrollments: List[YearPlan];
    done: List[str];

class Term(TypedDict):
    year: int
    term: int

class Course(TypedDict):
    code: str;
    name: str;
    units: int;
    terms: List[Term];
    prereqs: str;
    coreqs: str;
    exclusions: str;
    equivalents: str;

CourseList = List[Course]

class CourseReq(TypedDict):
    filter_type: str;
    info: List[str];

class CheckResponse(TypedDict):
    degree_reqs: List[RemainReq]; # list of requirements for nonspecific courses (gen eds, free elecs)
    course_reqs: Dict[str, List[CourseReq]];
    course_warn: Dict[str, List[str]];

class GeneratorResponse(TypedDict):
    program: Program;
    courses: Dict[str, Course];
    reqs: CheckResponse;
    full_reqs: List[RemainReq];

