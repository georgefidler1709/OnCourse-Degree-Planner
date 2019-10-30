.mode csv
.import 'courses.csv' Courses
update Courses set prereq = NULL where prereq = "";
update Courses set coreq = NULL where coreq = "";
update Courses set exclusion = NULL where exclusion = "";
update Courses set equivalent = NULL where equivalent = "";