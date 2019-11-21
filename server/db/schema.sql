create table Degrees (
    name varchar(100),
    faculty varchar(100),
    duration integer,
    id integer primary key
);

create table DegreeOfferings (
    year integer,
    degree_id integer references Degrees(id),
    primary key (year, degree_id)
);

create table Courses (
    letter_code char(4),
    number_code char(4),

    level integer required check (level >= 0),

    name varchar(100),
    faculty varchar(100),
    units integer required check(units >= 0),

    prereq integer references CourseRequirements(id),
    coreq integer references CourseRequirements(id),

    finished integer required,

    id integer primary key,

    check (level <= 9),
    unique (letter_code, number_code)
);

create table Sessions (
    year integer,
    -- treat summer term as term 0
    term integer check (term >= 0),
    check (term <= 3),
    primary key (year, term)
);

create table CourseFilters (
    type_id integer references CourseFilterTypes(id),

    -- Specific Course filter
    min_mark integer,
    course_id integer references Courses(id),

    -- Gen Ed filter has no attributes

    -- Field filter
    field_code char(4),

    -- Level filter
    level integer,

    -- Free Elective Filter has no attributes

    id integer primary key,
    -- And and Or filters have relationships in CourseFilterHierarchies
    unique(min_mark, course_id)
);

-- For And and Or filters, the parent is the And/Or and the child is another filter
create table CourseFilterHierarchies (
    parent_id integer references CourseFilters(id),
    child_id integer references CourseFilters(id),

    primary key (parent_id, child_id)
);

create table CourseRequirements (
    type_id integer references CourseRequirementTypes(id),

    -- Completed Course requirement
    min_mark integer,
    course_id integer references Courses(id),

    -- Current Degree Requirement
    degree_id integer references Degrees(id),

    -- Year requirement
    year integer,

    -- UoC Requirement
    uoc_amount_required integer,
    uoc_min_level integer,
    uoc_subject char(4),
    uoc_course_filter integer references CourseFilters,

    -- wam requirement
    wam integer,

    id integer primary key,
    -- And and Or requirements have relationships in CourseRequirementHierarchies


    unique(type_id, min_mark, course_id),
    unique(type_id, degree_id),
    unique(type_id, year),
    unique(type_id, wam),
    unique(type_id, uoc_amount_required, uoc_min_level, uoc_subject, uoc_course_filter)
);

-- For And and Or requirements, the parent is the And/Or and the child is another requirement
create table CourseRequirementHierarchies (
    parent_id integer references CourseRequirements(id),
    child_id integer references CourseRequirements(id),

    primary key (parent_id, child_id)
);

create table DegreeOfferingRequirements (

    offering_degree_id integer required references DegreeOfferings(degree_id),
    offering_year_id integer required references DegreeOfferings(year),
    requirement_id integer required references CourseFilters(id),
    uoc_needed integer required check(uoc_needed > 0),
    alt_text text,
    id integer primary key
);

-- For degree offering requirements that are hard to make formulaic, make it a string for front-end
-- i.e. "60 days of Industrial Training" or 
-- "courses chosen must have at least 30 UOC level 4+ COMP courses"
create table DegreeOfferingNotes (
    offering_degree_id integer required references DegreeOfferings(degree_id),
    offering_year_id integer required references DegreeOfferings(year),
    note text required,
    id integer primary key
);

create table CourseOfferings (
    course_id integer references Courses(id),
    session_year integer references Sessions(year),
    session_term integer references Sessions(term),
    primary key (course_id, session_year, session_term)
);

create table EquivalentCourses (
    first_course integer references Courses(id),
    second_course integer references Courses(id),

    check (first_course < second_course),

    primary key (first_course, second_course)
);

create table ExcludedCourses (
    first_course integer references Courses(id),
    second_course integer references Courses(id),

    check (first_course < second_course),

    primary key (first_course, second_course)
);

create table CourseRequirementTypes (
    name varchar(100) unique,
    id integer primary key
);

create table CourseFilterTypes (
    name varchar(100) unique,
    id integer primary key
);
