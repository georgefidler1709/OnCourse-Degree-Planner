# COMP4920 19T3 - On Course

This is an app that aims to help UNSW students plan their degrees in an interactive manner. Features include:

* interactive drag-and-drop interface to plan courses on a timeline
* requirements checking for course prerequisites, corequisites, exclusions, equivalents
* requirements checking for degree program rules
* scraping scripts to get course data from the handbook, parsing rules to interpret data
* framework to input degree program rules

Currently, the framework exists to scrape courses from the entire handbook. Not all requirements are able to be interpreted fully, but the parsed data is displayed on the frontend and the course is highlighted in yellow to allow user checking. A framework exists to update course requirements using a `.txt` file that is formatted in a user-friendly way.

Degrees that are currently in the database are 3778 (COMPA1), 3707 (SENGAH, BINFAH, COMPBH), 3502 (ACCTA1, FINSA1), 3970 (BIOSJ1, MATHT1, PSYCA1). The current courses in the database would support the addition of any 3502 Commerce or 3970 Science major stream. Capabilities to support other degrees would require scraping for more courses, which was not done at this point in time due to its time-consuming nature.

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
* Run `./start.sh init-db` to re-set the database and just scrape courses. 
	* To add more fields to scrape for courses, modify the list `FIELDS_TO_SCRAPE` in `./server/db_setup.py`'s `do_init_db()` function.
* Run `./start.sh add-to-db` to add manual course and degree requirements.

# Running the Application

0. Make sure the database `./server/db/university.db` is generated and populated if changes have been made.
1. In one terminal, `. venv/bin/activate` `&&` `./start.sh run` to run the API on `localhost:5000`
2. In another terminal, `cd frontend` `&&` `npm start` to run the frontend on `localhost:3000`

# Testing

## Mypy

run `mypy .` for type checking

## Pytest

Test are located in `./classes/tests` folder. Add the line `export PYTHONPATH=./classes:$PYTHONPATH` to the last line of your `venv/bin/activate` file. This way you can just `import degree` from anywhere (including in the test files).

Run pytest from the root folder with

```
pytest --pyargs classes
```

Extra options
* `-s` to capture stdout even if test passes (anything you `print()`)
