'''
Version of query_db function to pass into University
that connects to db without flask g, so you can query
db offline (i.e. without flask app running)
'''
from typing import Tuple
import sqlite3

conn = sqlite3.connect('./server/db/university.db', detect_types=sqlite3.PARSE_DECLTYPES)
conn.row_factory = sqlite3.Row

def query_db(query : str, args: Tuple = (), one = False) -> sqlite3.Row:
    # query function from flask documentation
    # https://flask.palletsprojects.com/en/1.1.x/patterns/sqlite3/#easy-querying

    cur = conn.execute(query, args)
    rv = cur.fetchall()
    return (rv[0] if rv else None) if one else rv