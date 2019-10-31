from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash, jsonify
from typing import List, Set, Dict, Tuple, Optional
from classes.university import University
from classes.degree import Degree
from classes.generator import Generator

from .db_setup import query_db

degrees_bp = Blueprint("degrees_bp", __name__,
    template_folder='templates', static_folder='static');

@degrees_bp.route('/degrees.json')
def load_degrees() -> str:
    '''
    Loads a dict of degree choices
    '''
    uni = University(query_db)

    return jsonify(uni.get_simple_degrees())

@degrees_bp.rotue('/<code>/gen_program.json')
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

    gen = Generator(deg)  

    # TODO uncomment this when you make this function
    # need to add an API type and return that in gen.generate_api()
    
    return jsonify(gen.generate().to_api())

#@hello_bp.route('/', methods=['GET', 'POST'])
#def hello() -> str:
#    # need to have a list of degrees
#    # query db for possible degrees
#    degrees = load_degrees()
#
#    if request.method == "POST":
#        # TODO validate the degree chosen is in our db
#        
#        code = request.form.get('degree', None)
#        
#        if code is None:
#            flash("You need to enter a degree code")
#            return render_template('hello.html', degrees=degrees)
#
#        return redirect(url_for('hello_bp.plan', code=code))
#
#
#    # TODO render autocomplete in js like: https://dev.to/sage911/how-to-write-a-search-component-with-suggestions-in-react-d20
#    return render_template('hello.html', text='hello world', degrees=degrees);

#@degrees_bp.route('/plan/<code>', methods=['GET'])
#def plan(code : int) -> str:
#
#    return f"You selected degree {code}"
