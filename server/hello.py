from flask import Blueprint, render_template, g, current_app
from typing import List, Set, Dict, Tuple, Optional

hello_bp = Blueprint("hello_bp", __name__,
    template_folder='templates', static_folder='static');

def query_db(query : str, args: Tuple = (), one = False) -> Tuple:
    # query function from flask documentation
    # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

    # ERROR can't access g.db this way..? HOW TO ACCESS G.DB
    print(f"g.db = {g.db}")
    with current_app.app_context():
        cur = g.db.execute(query, args)
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

@hello_bp.route('/', methods=['GET'])
def hello() -> str:
    # need to have a list of degrees
    print(f"g.keys = {g.keys()}")
    # query db for possible degrees
    degrees = load_degrees()

    # TODO render autocomplete in js like: https://dev.to/sage911/how-to-write-a-search-component-with-suggestions-in-react-d20
    return render_template('hello.html', text='hello world', degrees=degrees);
