import React, {MouseEvent} from "react";
import SuggestionInfoHover from "./SuggestionInfoHover"
import { useHistory } from "react-router-dom";
import { Course } from '../../Api'
import {Position, SearchResult, CourseSearchResult} from '../../Types'
import styled from 'styled-components'

const Suggestion = styled.button`
  border: 1px solid #575756;
  border-radius: 10px;
  padding: 10px;
  margin-bottom: 8px;
  width: 220px;
  background-color: #c2eced;
`

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`
const Code = styled.h1`
  pointer-events: none;
`

const Name = styled.p`
  pointer-events: none;
`

const CourseSuggestion = styled.button`
  border: 1px solid #cccccc;
  border-radius: 10px;
  padding: 0px;
  margin-bottom: 5px;
  width: 95%;
  background-color: white;
`

const CourseCode = styled.p`
  margin: 3px;
  pointer-events: none;
`

const CourseName = styled.small`
  pointer-events: none;
`


function Suggestions(props: {degrees: Array<SearchResult>}) {

  const year : string = "2020"
  const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/programs/${year}/`
  const placement : Position = "right"
  let history = useHistory();

  function handleClick(event: MouseEvent<HTMLButtonElement>) {
    history.push("/" + event.currentTarget.id.toString())
  }
  
  const options = props.degrees.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.degree.id}>More Info</a>
      }
      placement={placement}
      delay={200}
      key={r.degree.id}
    >
      <Suggestion
        id={r.degree.id}
        value={r.degree.id}
        onClick={handleClick}
      >
        <Code>{r.degree.id}</Code>
        <Name>{r.text}</Name>
      </Suggestion>
    </SuggestionInfoHover>
    
  ));

  return <Container>{options}</Container>;
}

export default Suggestions;
export { Suggestions };

interface CourseSuggestionsProps {
  courses: Array<CourseSearchResult>;
  add_event: (course: Course) => void;
}

function CourseSuggestions(props: CourseSuggestionsProps) {

  const year : string = "2020"
  const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/courses/${year}/`
  const placement : Position = "right"
  
  const options = props.courses.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.course.code}>More Info</a>
      }
      placement={placement}
      delay={200}
      key={r.course.code}
    >
      <CourseSuggestion
        id={r.course.code}
        value={r.course.code}
        onClick={() => props.add_event(r.course)}
      >
        <CourseCode>{r.code}</CourseCode>
        <CourseName>{r.text}</CourseName>
      </CourseSuggestion>
    </SuggestionInfoHover>
    
  ));

  return <Container>{options}</Container>;
}

export { CourseSuggestions };