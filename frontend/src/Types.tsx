import { GeneratorResponse, Program, TermPlan, YearPlan, SimpleDegree, SimpleCourse, Course } from "./Api"
import styled from 'styled-components';

export const SubTitle = styled.h5`
  padding: 4px;
  font-family: Arial, Helvetica, sans-serif;
`;

export type Position = "auto-start" | "auto" | "auto-end" | "top-start" | "top" | "top-end" | "right-start" | "right" | "right-end" | "bottom-end" | "bottom" | "bottom-start" | "left-end" | "left" | "left-start"

export interface TimelineState extends GeneratorResponse {
  accepted_overload: boolean;
  program: ProgramState;
  add_course: Array<string>; // course to add, usually undefined
}

export interface ProgramState extends Program {
  enrollments: Array<YearState>;
}

export interface YearState extends YearPlan {
  term_plans: Array<TermState>
}
export interface TermState extends TermPlan {
  highlight: boolean;
}
export interface SearchResult {
  degree: SimpleDegree 
  text: JSX.Element 
  code: JSX.Element
}

export interface CourseSearchResult {
  course: SimpleCourse
  text: JSX.Element
  code: JSX.Element
}

export type addCallbackType = (course: Course) => void;

export interface Req {
  filter_type: string;
  units: number;
  info: string;
}
