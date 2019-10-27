#!/bin/sh
db='university.db'

sqlite3 $db < schema.sql
sqlite3 $db < setup_enums.sql

sqlite3 $db < data.sql

# will have an error reading line 1 as that's the header line
sqlite3 'university.db' <<EOF
.mode csv
.import courses.csv Courses
update Courses set prereq = NULL where prereq = "";
update Courses set coreq = NULL where coreq = "";
update Courses set exclusion = NULL where exclusion = "";
update Courses set equivalent = NULL where equivalent = "";
EOF