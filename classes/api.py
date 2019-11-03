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

from typing import List
from mypy_extensions import TypedDict

class SimpleDegree(TypedDict):
    id: int;
    name: str;

SimpleDegrees = List[SimpleDegree]

class Term(TypedDict):
    year: int
    term: int

class Course(TypedDict):
    subject: str;
    code: int;
    name: str;
    units: int;
    terms: List[Term];

class CourseEnrollment(TypedDict):
    course: Course;
    term: Term;

class RemainReq(TypedDict):
    units: int;
    filter_type: str;

class Program(TypedDict):
    # Degree object
    id: int;
    name: str;
    year: int;
    duration: int; # in years
    url: str; # degree handbook url
    reqs: List[RemainReq]; # list of requirements for nonspecific courses (gen eds, free elecs)

    # List of CourseEnrollments
    enrollments: List[CourseEnrollment];
