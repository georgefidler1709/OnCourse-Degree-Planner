from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash, jsonify
from typing import List, Set, Dict, Tuple, Optional
import json

from classes.university import University
from classes.degree import Degree
from classes.generator import Generator
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


def prog_api_to_class(prog: api.Program) -> program.Program:
    '''
    Given an API Program (json format), converts it to a new program
    '''
    # TODO
    pass

@degrees_bp.route('/check_program.json', methods=['POST'])
def check_program() -> str:
    '''
    Accepts a program from the front-end. This program has courses
    in a new position.
    Return a jsonified program that has an annotation for each course
    about whether or not it's valid.
    '''
    print("----------- request ------------")
    # print(request)
    # print(f"request.is_json = {request.is_json}")
    # print(f"request.args = {request.args}")
    # print(f"request.json = {request.json}")
    # print(f"request.get_json() = {request.get_json()}")
    # print(f"request.data = {request.data!r}")
    json_data = json.loads(request.data)
    print(f"json_data = {json_data}")

    # raise Exception('Pause here')

    # create a new classes.program
    # uni = University(query_db)

    # deg = uni.load_degree(prog['id'])

    # new: program.Program = program.Program(deg, prog['enrollments'])

    # TODO replace
    return json_data
