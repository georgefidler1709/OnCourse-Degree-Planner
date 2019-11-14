import { GeneratorResponse, Program, TermPlan, YearPlan, SimpleDegree, Course} from "./Api"

export type Position = "auto-start" | "auto" | "auto-end" | "top-start" | "top" | "top-end" | "right-start" | "right" | "right-end" | "bottom-end" | "bottom" | "bottom-start" | "left-end" | "left" | "left-start"

export interface TimelineState extends GeneratorResponse {
    program: ProgramState;
    add_course: Course; // course to add, usually undefined
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
}

export interface CourseSearchResult {
  course: Course
  text: JSX.Element
  code: JSX.Element
}

export type addCallbackType = (course: Course) => void;
