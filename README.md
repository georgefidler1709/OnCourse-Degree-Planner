# COMP4920 On Course

# Virtual Environment

* `virtualenv --python=python3.7 venv` (`venv` is in `.gitignore`)
* `. venv/bin/activate`
* `pip3 install -r requirements.txt`

If you add packages make sure you add it to requirements.txt by doing `pip3 freeze > requirements.txt`. 


# Mypy

run `mypy .` for type checking

# Run Flask Server

From root folder, run `./start.sh run`. 

# Regenerate Database

From root folder, run `./start.sh db-init`. 
