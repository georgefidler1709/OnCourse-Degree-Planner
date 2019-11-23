# COMP4920 19T3 - On Course

Group Members

* Alexander Rowell (z5116848)
* Eleni Dimitriadis (z5191013)
* Emily Chen (z5098910)
* George Fidler (z5160384)
* Kevin Ni (z5025098)

# Virtual Environment

* `virtualenv --python=python3.7 venv` (`venv` is in `.gitignore`)
  * on CSE, you have to do a user install of `virtualenv`
  * `pip3 install --user virtualenv`, CSE python 3 is python 3.7
  * `python3 -m venv venv`
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`

If you add packages make sure you add it to requirements.txt by doing `pip3 freeze > requirements.txt`. 


# Mypy

run `mypy .` for type checking

# Run Flask Server

Make sure `./server/db/university.db` exists. Otherwise first run `./start.sh init-db-full`.

From root folder, run `./start.sh run`. 

# Run Static Server (development mode)

From frontend folder run `npm start`. this only needs to be done once. see `/frontend/README.md` for details

# Regenerate Database

Run `./start.sh init-db-full` to generate the full database, including manually added degrees and course
requirements.

If you only want things that were scraped and parsed from the handbook, run `./start.sh init-db`.

If you have a database with only the scraped things and want to add the manual things, run
`./start.sh add-to-db`.


# Pytest

Test are located in `./classes/tests` folder. Add the line `export PYTHONPATH=./classes:$PYTHONPATH` to the last line of your `venv/bin/activate` file. This way you can just `import degree` from anywhere (including in the test files).

Run pytest from the root folder with

```
pytest --pyargs classes
```

Extra options
* `-s` to capture stdout even if test passes (anything you `print()`)
