from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash, jsonify
from typing import List, Set, Dict, Tuple, Optional
from classes.university import University

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
