// IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE classes/api.py TO MATCH

export interface SimpleDegree {
    id: string; 
    name: string;
}

export type SimpleDegrees = Array<SimpleDegree>;

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

export interface Program {
    // Degree object
    id: number;
    name: string;
    year: number;
    duration: number; // in years
    url: string; // handbook entry for degree
    enrollments: Array<CourseEnrollment>;
}
