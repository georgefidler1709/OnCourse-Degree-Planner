# IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE frontend/src/Api.tsx TO MATCH 
import json;

"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

apiTypes.py
Contains the json layout of the types to be sent over to the front end
"""

from typing import List, Dict
from mypy_extensions import TypedDict

class SimpleDegree(TypedDict):
    id: str;
    name: str;

SimpleDegrees = List[SimpleDegree]

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

class CourseReq(TypedDict):
    filter_type: str;
    # list of conditions / courses
    info: str;

class RemainReq(CourseReq):
    units: int;

class Program(TypedDict):
    # Degree object
    id: int;
    name: str;
    year: int;
    duration: int; # in years
    url: str; # degree handbook url
    reqs: List[RemainReq]; # list of requirements for nonspecific courses (gen eds, free elecs)

    # List of CourseEnrollments
    enrollments: List[YearPlan];

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

class GeneratorResponse(TypedDict):
    program: Program;
    courses: Dict[str, Course];

class CheckResponse(TypedDict):
    degree_reqs: List[RemainReq];
    course_reqs: Dict[str, List[CourseReq]];

