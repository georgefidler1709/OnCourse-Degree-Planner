-- Using the 2019 handbook

insert into Degrees(name, id) values ('Science', 7001);
insert into Degrees(name, id) values ('Engineering', 7002);

-- Computer Science 3778, COMPA1
-- https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778

insert into Degrees(name, id) values ('Computer Science', 3778);
insert into DegreeOfferings(year, degree_id) values (2019, 3778);

-- -- TODO insert into courses
-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ('DPST', '1091', 1, 'Introduction to Programming', NULL, NULL, NULL, 1);
-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ('COMP', '1511', 1, 'Programming Fundamentals', NULL, NULL, NULL, 2);
-- update Courses set exclusion = 2 where id = 1;
-- update Courses set exclusion = 1 where id = 2;
-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ('DPST', '1092', 1, 'Computer System Fundamentals', NULL, NULL, NULL, 3);
-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ('COMP', '1521', 1, 'Computer System Fundamentals', 1, NULL, NULL, 4);
-- update Courses set exclusion = 4 where id = 3;
-- update Courses set exclusion = 3 where id = 4;
-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ();

-- -- DPST* courses are "UNSW Global Diploma only", but this is BOTH 7001 and 7002
-- insert into CourseRequirements(type_id, course_id, degree_id, id) values (2, 1, 7001, 1);
-- insert into CourseRequirements(type_id, course_id, degree_id, id) values (2, 1, 7002, 2);
-- insert into CourseRequirements(type_id, course_id, degree_id, id) values (2, 3, 7001, 3);
-- insert into CourseRequirements(type_id, course_id, degree_id, id) values (2, 3, 7002, 4);

-- -- pass COMP1511
-- insert into CourseRequirements(type_id, min_mark, course_id, id) values (1, 50, 2, 5);

-- insert into Courses(letter_code, number_code, level, name, prereq, coreq, exclusion, id) values ();


-- CourseFilters
-- insert into CourseFilters(type_id, min_mark, course_id, degree_id, year) values (1, 50, )