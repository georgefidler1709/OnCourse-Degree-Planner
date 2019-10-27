from flask import Blueprint, render_template, g, current_app, request, redirect, url_for, flash
from typing import List, Set, Dict, Tuple, Optional

from .db_setup import get_db

hello_bp = Blueprint("hello_bp", __name__,
    template_folder='templates', static_folder='static');

def query_db(query : str, args: Tuple = (), one = False) -> Tuple:
    # query function from flask documentation
    # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def load_degrees() -> Dict[int, str]:
    '''
    Loads a dict of degree choices
    '''
    # TODO might need to change the return type based on the javascript equivalent
    res = {}
    for degree in query_db('SELECT id, name FROM Degrees ORDER BY id'):
        res.update({degree['id'] : degree['name']})

    return res

@hello_bp.route('/', methods=['GET', 'POST'])
def hello() -> str:
    # need to have a list of degrees
    # query db for possible degrees
    degrees = load_degrees()

    if request.method == "POST":
        # TODO validate the degree chosen is in our db
        
        code = request.form.get('degree', None)
        
        if code is None:
            flash("You need to enter a degree code")
            return render_template('hello.html', degrees=degrees)

        return redirect(url_for('hello_bp.plan', code=code))


    # TODO render autocomplete in js like: https://dev.to/sage911/how-to-write-a-search-component-with-suggestions-in-react-d20
    return render_template('hello.html', text='hello world', degrees=degrees);

@hello_bp.route('/plan/<code>', methods=['GET'])
def plan(code : int) -> str:

    return f"You selected degree {code}"