/**
* IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE classes/api.py TO MATCH
*
* COMP4290 Group Project
* Team: On Course
* Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
* George Fidler (z5160384), Kevin Ni (z5025098)
* 
* Api.tsx
* Type interfaces for the objects received from calls to the backend
*/

// IF YOU EDIT THIS FILE MAKE SURE YOU UPDATE classes/api.py TO MATCH

/**
 * compact representation of degree for searching
 */
export interface SimpleDegree {
  id: string; 
  name: string;
  years: Array<number>;
}

export type SimpleDegrees = Array<SimpleDegree>;

export interface Term {
  year: number;
  term: number;
}

/**
 * compact representation of course for searching
 */
export interface SimpleCourse{
  code: string; 
  name: string;
  terms: Array<Term>;
}

export type CourseList = Array<SimpleCourse>;

/**
 * representation of courses taken in a term
 */
export interface TermPlan {
  course_ids: Array<string>;
  term: number;
}

/**
 * representation of courses taken in a year
 */
export interface YearPlan {
  term_plans: Array<TermPlan>;
  year: number;
}

/**
 * representation of remaining degree requirement
 */
export interface RemainReq {
  filter_type: string;
  info: string;
  units: number;
}

/**
 * representation of all courses taken in a particular degree
 */
export interface Program {
  // Degree information
  id: string;
  name: string;
  year: number;
  duration: number; // in years
  url: string; // handbook entry for degree

  notes: Array<string>;
  enrollments: Array<YearPlan>;
  done: Array<string>;
}

/**
 * detailed representation of a course
 */
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

export interface CourseReq {
  filter_type: string;
  info: Array<string>;
}

export interface CheckResponse{
  degree_reqs: Array<RemainReq>;
  course_reqs: {[index: string]: Array<CourseReq>};
  course_warn: {[index: string]: Array<string>};
}

export interface GeneratorResponse {
  program: Program;
  courses: {[index: string]: Course};
  reqs: CheckResponse;
  full_reqs: Array<RemainReq>;
}

