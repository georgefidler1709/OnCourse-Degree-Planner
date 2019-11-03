// IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE classes/api.py TO MATCH

export interface SimpleDegree {
    id: string; 
    name: string;
}

export type SimpleDegrees = Array<SimpleDegree>;

export interface SimpleCourse{
    id: string; 
    name: string;
}

export type SimpleCourses = Array<SimpleCourse>;

export interface Term {
    year: number;
    term: number;
}

export interface Course {
    subject: string;
    code: number;
    name: string;
    units: number;
    terms: Array<Term>;
}

export interface CourseEnrollment {
    course: Course;
    term: Term;
}

export interface RemainReq {
    units: number;
    filter_type: string;
}

export interface Program {
    // Degree object
    id: number;
    name: string;
    year: number;
    duration: number; // in years
    url: string; // handbook entry for degree
    reqs: Array<RemainReq>
    enrollments: Array<CourseEnrollment>;
}
