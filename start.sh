# Run flask server for On Course

export FLASK_APP=run.py
export FLASK_ENV=development
export APP_CONFIG_FILE=config.py

# add classes folder to path to import with classes.<file_name> from anywhere
export PATH=./classes:$PATH

# TODO change me!
export SECRET_KEY="OneTwoThreeFourFiveSix"

# set up the database connection
export DATABASE="./server/db/university.db"

export EXTRA_REQUIREMENTS='./server/db/extra_course_requirements.txt'

mypy . && flask $1
