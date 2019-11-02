'''
Set up Flask connection to database
https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
'''

from typing import Tuple

import os
import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
# from db import input_data
# from server.db import input_data

import classes.university

def query_db(query : str, args: Tuple = (), one = False) -> sqlite3.Row:
    # query function from flask documentation
    # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(err : Exception = None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db() -> None:
    '''
    Initialize db and populate it with information
    '''
    from server.db import input_data
    import pandas

    db_path = current_app.config['DATABASE']

    if os.path.exists(db_path):
        os.remove(db_path)

    db = get_db()

    with current_app.open_resource('db/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('db/setup_enums.sql') as f:
        db.executescript(f.read().decode('utf8'))

    with current_app.open_resource('db/data.sql') as f:
        db.executescript(f.read().decode('utf8'))

    # read courses from courses.csv
    courses = pandas.read_csv("server/db/courses.csv")
    courses.to_sql("Courses", db, if_exists="append", index=False)

    # input Computer Science 3778 COMPA1 course requirements
    input_data.compsci_course_reqs(db_path)

    # input Sessions for arbitrary range of years
    input_data.insert_sessions(start=2019, end=2025, db=db_path)

    # input CourseOfferings for 3778 COMPA1 courses
    input_data.insert_course_offerings(start=2019, end=2025, db=db_path)

    # input CourseFilters and DegreeOfferingRequirements for 3778 COMPA1
    input_data.insert_compsci_degree_requirements(db=db_path)


    # Temporary pseudo-testing just to make sure loading from db works
    '''
    uni = classes.university.University([], [])

    degree = uni.find_degree_number_code(3778)
    print(repr(degree))

    course = uni.find_course("COMP1511")

    print(repr(course))

    course = uni.find_course("COMP2511")
    print(repr(course))
    '''

def init_app(app : Flask) -> None:
    '''
    Init database for given flask app
    '''

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
