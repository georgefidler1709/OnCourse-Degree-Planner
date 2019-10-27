'''
Set up Flask connection to database
https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
'''
import os
import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext
import pandas

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(err : str = None) -> None:
    db = g.pop('db', None)

    if db is not None:
        db.close()

@click.command('init-db')
@with_appcontext
def init_db() -> None:
    '''
    Initialize db and populate it with information
    '''
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

    # TODO input course requirements...




def init_app(app : Flask) -> None:
    '''
    Init database for given flask app
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
