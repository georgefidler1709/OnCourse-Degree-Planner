import {SimpleDegree, Course} from './Api'

export type Position = "auto-start" | "auto" | "auto-end" | "top-start" | "top" | "top-end" | "right-start" | "right" | "right-end" | "bottom-end" | "bottom" | "bottom-start" | "left-end" | "left" | "left-start"
  
export interface SearchResult {
  degree: SimpleDegree 
  text: JSX.Element 
}

export interface CourseSearchResult {
	course: Course
	text: JSX.Element
	code: JSX.Element
}