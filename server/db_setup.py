'''
Set up Flask connection to database
https://flask.palletsprojects.com/en/1.1.x/tutorial/database/
'''

from typing import Tuple

import os
import shutil
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

def store_db(command: str, args: Tuple = ()) -> int:
    # Store information in the database

    try:
        cur = get_db().cursor()
        cur.execute(command, args)

        insert_id = cur.lastrowid
        get_db().commit()
    except sqlite3.IntegrityError as e:
        print(f'Failed integrity error with command \'{command}\' and args \'{args}\'')
        raise e

    return insert_id

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

@click.command('init-db-full')
@with_appcontext
def init_db_full() -> None:
    '''
    Initialize db and populate it with both information scraped from the handbook and extra
    information
    '''
    do_init_db()
    do_add_to_db()


@click.command('add-to-db')
@with_appcontext
def add_to_db() -> None:
    '''
    Add extra manual information about courses
    '''
    do_add_to_db()

def do_add_to_db() -> None:
    from server.db import input_data

    db_path = current_app.config['DATABASE']

    START_YEAR = 2020
    END_YEAR = 2021

    input_data.insert_degrees_with_no_offerings(db=db_path)

    # input Computer Science 3778 COMPA1 course requirements
    # In case we missed requirements for some courses
    input_data.compsci_course_reqs(db_path)

    # input CourseFilters and DegreeOfferingRequirements for 3778 COMPA1
    input_data.insert_compsci_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    # insert requirements for SENGAH
    input_data.insert_seng_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    # bioinformatics
    input_data.insert_binf_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    # computer engineering
    input_data.insert_compeng_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    # commerce majors
    input_data.insert_fins_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)
    input_data.insert_acct_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    # science majors
    input_data.insert_stat_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)
    input_data.insert_psyc_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)
    input_data.insert_bio_degree_requirements(db=db_path, start_year=START_YEAR, end_year=END_YEAR)

    print('DEGREE REQUIREMENTS INSERTED')

@click.command('init-db')
@with_appcontext
def init_db() -> None:
    '''
    Initialize db and populate it with information scraped with the handbook
    '''
    do_init_db()

def do_init_db() -> None:
    from scraper import dbGenerator
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

    # Generate as much as we can from the handbook
    generator = dbGenerator.DbGenerator(query_db, store_db)

    # TODO: Change later if we decide to include multiple years or different study levels
    year = 2020
    postgrad = False

    COMP_DEG_FIELDS = ['COMP', 'MATH', 'ENGG', 'DESN', 'SENG', 'ELEC', 'INFS', 'TELE',
        'BABS', 'BIOC', 'MICR', 'CHEM', 'PHYS', 'BINF']
    COMMERCE_DEG_FIELDS = ['ACCT', 'ECON', 'MGMT', 'COMM', 'FINS', 'MARK', 'TABL', 
        'ACCT', 'BLDG', 'RISK']
    SCIENCE_DEG_FIELDS = ['ANAT', 'AVEN', 'AVIA', 'AVIF', 'AVIG', 'BABS', 'BEES', 'BIOC',
        'BIOS', 'BIOT', 'CLIM', 'FOOD', 'GEOS', 'MATS', 'MSCI', 'NEUR', 'OPTM', 'PATH',
        'PHAR', 'PHSL', 'PSYC', 'SCIF', 'SOMS', 'VISN']
    GENED_FIELDS = ['ARTS']

    ALL_FIELDS = COMP_DEG_FIELDS + COMMERCE_DEG_FIELDS + SCIENCE_DEG_FIELDS + GENED_FIELDS

    FIELDS_TO_SCRAPE = list(set(ALL_FIELDS))

    generator.generate_db(year, FIELDS_TO_SCRAPE, postgrad, end_year=2025)

    # read courses from courses.csv
    #courses = pandas.read_csv('server/db/courses.csv')
    #courses.to_sql('Courses', db, if_exists='append', index=False)

    # input Computer Science 3778 COMPA1 course requirements
    # In case we missed requirements for some courses
    #input_data.compsci_course_reqs(db_path)

    # input Sessions for arbitrary range of years
    #input_data.insert_sessions(start=2019, end=2025, db=db_path)

    # input CourseOfferings for 3778 COMPA1 courses
    #input_data.insert_course_offerings(start=2019, end=2025, db=db_path)

    shutil.copyfile(db_path, db_path + '_scraped')

    print('GENERATE DB + SCRAPE COURSES SUCCESSFUL')

def init_app(app : Flask) -> None:
    '''
    Init database for given flask app
    '''

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db)
    app.cli.add_command(add_to_db)
    app.cli.add_command(init_db_full)
