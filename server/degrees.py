from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash, jsonify
from typing import List, Set, Dict, Tuple, Optional
from classes.university import University
from classes.degree import Degree
from classes.generator import Generator

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

