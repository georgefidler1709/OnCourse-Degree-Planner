# COMP4920 19T3 - On Course

This is an app that aims to help UNSW students plan their degrees in an interactive manner. Features include:

* Interactive drag-and-drop interface to plan courses on a timeline
* Requirements checking for course prerequisites, corequisites, exclusions, equivalents
* Requirements checking for degree program rules
* Scraping scripts to get course data from the handbook, parsing rules to interpret data
* Framework to input degree program rules

Currently, the framework exists to scrape courses from the entire handbook. Not all requirements are able to be interpreted fully, but the parsed data is displayed on the frontend and the course is highlighted in yellow to allow user checking. A framework exists to update course requirements using a `.txt` file that is formatted in a user-friendly way.

Degrees that are currently in the database are 3778 (COMPA1), 3707 (SENGAH, BINFAH, COMPBH), 3502 (ACCTA1, FINSA1), 3970 (BIOSJ1, MATHT1, PSYCA1). The current courses in the database would support the addition of any 3502 Commerce or 3970 Science major stream. Capabilities to support other degrees would require scraping for more courses, which was not done at this point in time due to its time-consuming nature.

## Disclaimer

This application is a good tool for students. However, it is not UNSW-endorsed so does not replace official UNSW channels, such as submitting a [progression check](https://nucleus.unsw.edu.au/Program/academic-progression-and-progression-checks). 

## Group Members

* Alexander Rowell (z5116848)
* Eleni Dimitriadis (z5191013)
* Emily Chen (z5098910)
* George Fidler (z5160384)
* Kevin Ni (z5025098)

# Setup

## Virtual Environment

Create a virtual environment and install the required packages as follows. We use python 3.7. 

* `virtualenv --python=python3.7 venv` (`venv` is in `.gitignore`)
  * on CSE, you have to do a user install of `virtualenv`
  * `pip3 install --user virtualenv`, CSE python 3 is python 3.7
  * `python3 -m venv venv`
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`

If you add packages make sure you add it to requirements.txt by doing `pip3 freeze > requirements.txt`. 

## Frontend Development Environment

The frontend will have to be run from the `./frontend/` folder. See `./frontend/README.md` for instructions on how to install `npm` and `node` to run the server.

## Database

`sqlite3` must be installed.

A populated sqlite3 database is located at: `./server/db/university.db`. The schema is located at `./server/db/schema.sql`.

If you wish to re-generate the database, you may either:

* Run `./start.sh init-db-full` to generate the full database, including scraped courses and manual degree requirements.

Or 

* Run `./start.sh init-db` to re-set the database and just scrape courses. 
	* To add more fields to scrape for courses, modify the list `FIELDS_TO_SCRAPE` in `./server/db_setup.py`'s `do_init_db()` function.
* Run `./start.sh add-to-db` to add manual course and degree requirements.

# Running the Application

0. Make sure the database `./server/db/university.db` is generated and populated if changes have been made.
1. In one terminal, `. venv/bin/activate` `&&` `./start.sh run` to run the API on `localhost:5000`
2. In another terminal, `cd frontend` `&&` `npm start` to run the frontend on `localhost:3000`

# Framework

## Languages

* Backend functions are written in **Python 3.7** (**mypy** for type-checking).
* API is served using **Flask** for python.
* Frontend is served using **React** and **TypeScript** for type-checking.

## Package Structure


    .
    ├── classes                   # Backend classes
    ├── documentation             # Design documents
    ├── frontend                  # Frontend development environment
    ├── scraper                   # Python clases to scrape and parse the handbook
    ├── server                    # Serving the API and database setup
    ├── tests                     # Pytest files for the backend
    ├── config.py                 # Sets environment variables
    ├── README.md
    ├── requirements.txt     
    ├── run.py                    # Initializes Flask API
    └── start.sh                  # Exports environment variables and runs Flask app, data generation commands


## Adding to the Database

### Scrape More Courses

1. Set the fields you want to scrape in the list `FIELDS_TO_SCRAPE` in `./server/db_setup.py`'s `do_init_db()` function.
2. Run `./start.sh init-db-full` (also adds manual requirements) or `./start.sh init-db` (only scrapes). WARNING, this resets the database. Make a copy of previous database if you wish.

### Manually Update Course Requirements

TODO

### Input New Degrees

1. Add a function to `./server/db/input_data.py` to input requirements for that degree.
	* `def insert_x_degree_requirements(db='university.db', start_year=2020, end_year=2021)` is a recommended signature
2. Use the functions available in `./server/db/helper.py`'s `Helper` class to input requirements.
3. Add a call to this function in `./server/db_setup.py`'s `do_add_to_db()` function.

# Testing

## Backend

### Mypy

Run `mypy .` from the home folder for type-checking. It is also integrated into the `./start.sh` script.

### Pytest

Test are located in the `./classes/tests` folder. Add the line `export PYTHONPATH=./classes:$PYTHONPATH` to the last line of your `venv/bin/activate` file. This way you can just `import degree` from anywhere (including in the test files).

Run pytest from the root folder with

```
pytest --pyargs tests
```

Extra options
* `-s` to capture stdout even if test passes (anything you `print()`)

## Frontend

Tests are located in the `./frontend/src/__tests__` folder. 

Run tests from `./frontend` with

```
npm test a
```
