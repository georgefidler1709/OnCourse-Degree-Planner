# script to input Courses into the database
# using sqlite3

# will have an error on line 1 as that's the header line

sqlite3 'university.db' <<EOF
.mode csv
.import courses.csv Courses
update Courses set prereq = NULL where prereq = "";
update Courses set coreq = NULL where coreq = "";
update Courses set exclusion = NULL where exclusion = "";
update Courses set equivalent = NULL where equivalent = "";
EOF