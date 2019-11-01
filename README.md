# COMP4920 On Course

# Virtual Environment

* `virtualenv --python=python3.7 venv` (`venv` is in `.gitignore`)
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`

If you add packages make sure you add it to requirements.txt by doing `pip3 freeze > requirements.txt`. 


# Mypy

run `mypy .` for type checking

# Run Flask Server

Make sure `./server/db/university.db` exists. Otherwise first run `./start.sh init-db`.

From root folder, run `./start.sh run`. 

# Run Static Server (development mode)

From frontend folder run `npm start`. this only needs to be done once. see `/frontend/README.md` for details

# Regenerate Database

# Pytest

Test are located in `./classes/tests` folder. Add the line `export PYTHONPATH=./classes:$PYTHONPATH` to the last line of your `venv/bin/activate` file. This way you can just `import degree` from anywhere (including in the test files).

Run pytest from the root folder with

```
pytest --pyargs classes
```
