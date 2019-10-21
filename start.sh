# Run flask server for On Course

export FLASK_APP=run.py
export FLASK_ENV=development

# add classes folder to path to import with classes.<file_name> from anywhere
export PATH=./classes:$PATH

# TODO change me!
export SECRET_KEY="OneTwoThreeFourFiveSix"

flask run