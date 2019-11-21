-- Using the 2019 handbook

insert into Degrees(name, faculty, duration, id) values ('Science', 'Science', 3, 7001);
insert into Degrees(name, faculty, duration, id) values ('Engineering', 'Engineering', 3, 7002);

-- Computer Science 3778, COMPA1
-- https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778

insert into Degrees(name, faculty, duration, id) values ('Computer Science', 'Engineering', 3, 3778);

insert into DegreeOfferings(year, degree_id) values (2020, 3778);
insert into DegreeOfferings(year, degree_id) values (2021, 3778);

-- insert courses from csv file
-- Google sheet in Google Drive: Project/Database Input/Courses Table
-- downloaded as csv as courses.csv
