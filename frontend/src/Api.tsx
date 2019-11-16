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

export interface TermPlan {
  course_ids: Array<string>;
  term: number;
}

export interface YearPlan {
  term_plans: Array<TermPlan>;
  year: number;
}

export interface RemainReq {
  filter_type: string;
  info: string;
  units: number;
}

export interface Program {
  // Degree object
  id: number;
  name: string;
  year: number;
  duration: number; // in years
  url: string; // handbook entry for degree
  reqs: Array<RemainReq>
    enrollments: Array<YearPlan>;
}

export interface Term {
  year: number;
  term: number;
}

export interface Course {
  code: string;
  name: string;
  units: number;
  terms: Array<Term>;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
}

export type CourseList = Array<Course>;

export interface GeneratorResponse {
  program: Program;
  courses: {[index: string]: Course};
}

export interface CourseReq {
  filter_type: string;
  info: Array<string>;
}

export interface CheckResponse{
  degree_reqs: Array<RemainReq>;
  course_reqs: {[index: string]: Array<CourseReq>};
}
