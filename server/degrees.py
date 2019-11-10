from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash, jsonify
from typing import List, Set, Dict, Tuple, Optional
import json

from classes.university import University
from classes.degree import Degree
from classes.generator import Generator
from classes.term import Term
from classes.courseEnrollment import CourseEnrollment
from classes import api
from classes import program

from .db_setup import query_db

degrees_bp = Blueprint("degrees_bp", __name__);

@degrees_bp.route('/degrees.json')
def load_degrees() -> str:
    '''
    Loads a dict of degree choices
    '''
    uni = University(query_db)

    return jsonify(uni.get_simple_degrees())

@degrees_bp.route('/courses.json')
def load_courses() -> str:
    '''
    Loads a dict of degree choices
    '''
    uni = University(query_db)
    return jsonify(uni.get_simple_courses())

@degrees_bp.route('/<code>/gen_program.json')
def generate_program(code: int) -> str:
    '''
    Generates a program plan for the given degree code, 
    '''
    uni = University(query_db)

    deg = uni.load_degree(code)

    if deg is None:
        # given code is not valid
        # TODO see if there's a more elegant way of doing this
        raise Exception(f"Degree code {code} is not in the database.")

    gen = Generator(deg, uni)

    return jsonify(gen.generate().get_generator_response_api())


def enrollments_api_to_classes(prog: api.Program, uni: University) -> List[CourseEnrollment]:
    # converts a jsonified version of api.Program
    # to a list of CourseEnrollments ready for Program's constructor
    enrollments = prog['enrollments']

    res = []

    for year_plan in enrollments:

        year = int(year_plan['year'])

        for term_plan in year_plan['term_plans']:

            term = int(term_plan['term'])

            for course in term_plan['course_ids']:

                course_data = uni.find_course(course)
                if course_data is None: continue # shouldn't happen

                term_data = Term(year, term)

                res.append(CourseEnrollment(course_data, term_data))

    return res

@degrees_bp.route('/check_program.json', methods=['POST'])
def check_program() -> str:
    '''
    Accepts a program from the front-end. This program has courses
    in a new position.
    Return a jsonified program that has an annotation for each course
    about whether or not it's valid.
    '''
    json_data = json.loads(request.data)
    data: api.Program = json_data

    # create a new classes.program
    uni = University(query_db)

    deg = uni.load_degree(data['id'])
    assert deg is not None
    enrollments = enrollments_api_to_classes(data, uni)

    new = program.Program(deg, enrollments)

    return jsonify(new.to_api())
