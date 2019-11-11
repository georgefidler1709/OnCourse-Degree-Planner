import { GeneratorResponse, Program, TermPlan, YearPlan} from "./Api"

export type Position = "auto-start" | "auto" | "auto-end" | "top-start" | "top" | "top-end" | "right-start" | "right" | "right-end" | "bottom-end" | "bottom" | "bottom-start" | "left-end" | "left" | "left-start"

export interface TimelineState extends GeneratorResponse {
    program: ProgramState;
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