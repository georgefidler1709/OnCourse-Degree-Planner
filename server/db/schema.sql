create table Degrees (
    name varchar(100),
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

    level integer required check (level > 0),

    name varchar(100),

    prereq integer references CourseRequirements(id),
    coreq integer references CourseRequirements(id),
    exclusion integer references CourseRequirements(id),

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
    id integer primary key
);

create table CourseRequirements (
    id integer primary key
);

create table OfferingRequirements (
    offering_id integer required references DegreeOfferings(id),
    requirement_id integer required references CourseRequirements(id),
    uoc_needed integer required check(uoc_needed > 0),
    id integer primary key
);

create table CourseOfferings (
    course_id integer references Courses(id),
    session_year integer references Sessions(year),
    session_term integer references Sessions(term),
    primary key (course_id, session_year, session_term)
);
