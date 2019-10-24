'''
Set up Flask connection to database
https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
'''
import os
import sqlite3
import click
from flask import current_app, g, Flask
from flask.cli import with_appcontext

def query_db(query : str, args: Tuple = (), one = False) -> Tuple:
    # query function from flask documentation
    # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_db() -> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        # Add an easier way to query the database
        g.query_db = query_db

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


def init_app(app : Flask) -> None:
    '''
    Init database for given flask app
    '''
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
