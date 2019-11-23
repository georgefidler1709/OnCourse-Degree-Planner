import React, {MouseEvent} from "react";
import SuggestionInfoHover from "./SuggestionInfoHover"
import { useHistory } from "react-router-dom";
import { Button } from 'react-bootstrap'
import {Position, SearchResult, CourseSearchResult} from '../../Types'
import { DEGREE_HANDBOOK_PREFIX, COURSE_HANDBOOK_PREFIX } from '../../Constants'
import styled from 'styled-components'

const DegreeSuggestion = styled(Button)`
  && {
    border: 1px solid #cccccc;
    border-radius: 10px;
  }
  margin-bottom: 1% 
  width: 70%;
  background-color: white;
`

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
`
const DegreeCode = styled.h1`
  font-size: 40px;
  pointer-events: none;
`

const DegreeName = styled.p`
  font-size: 20px;
  pointer-events: none;
`

const CourseSuggestion = styled(Button)`
  && {
    border: 1px solid #cccccc;
    border-radius: 10px;
  }
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


function Suggestions(props: {degrees: Array<SearchResult>, year: number}) {
  const placement : Position = "right"
  let history = useHistory();

  function handleClick(event: MouseEvent<HTMLButtonElement>, degree: string, year: number, years: Array<number>) {
    if(years.findIndex(y => y === year) === -1) {
      alert(`${degree} was not available in starting year: ${year}`)
      return
    }
    history.push("/" + event.currentTarget.id.toString() + "/" + year)
  }
  
  const options = props.degrees.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a 
          href={DEGREE_HANDBOOK_PREFIX + r.degree.id}
          target="_blank"
          rel="noopener noreferrer" 
        >More Info
        </a>
      }
      placement={placement}
      delay={100}
      key={r.degree.id}
      infoSize={{'fontSize': '25px'}}
    >
      <DegreeSuggestion
        variant="light"
        id={r.degree.id}
        value={r.degree.id}
        onClick={(e: MouseEvent<HTMLButtonElement>) => handleClick(e, r.degree.id, props.year, r.degree.years)}
      >
        <DegreeCode>{r.code}</DegreeCode>
        <DegreeName>{r.text}</DegreeName>
      </DegreeSuggestion>
    </SuggestionInfoHover>
    
  ));

  return <Container>{options}</Container>;
}

export default Suggestions;
export { Suggestions };

interface CourseSuggestionsProps {
  courses: Array<CourseSearchResult>;
  add_event: (code: string) => void;
}

function CourseSuggestions(props: CourseSuggestionsProps) {

  const placement : Position = "right"

  const options = props.courses.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a 
          href={COURSE_HANDBOOK_PREFIX + r.course.code}
          target="_blank"
          rel="noopener noreferrer" 
        >More Info
        </a>
      }
      placement={placement}
      delay={200}
      key={r.course.code}
      infoSize={{'fontSize': '14px'}}
    >
      <CourseSuggestion
        variant="light"
        id={r.course.code}
        value={r.course.code}
        onClick={() => props.add_event(r.course.code)}
      >
        <CourseCode>{r.code}</CourseCode>
        <CourseName>{r.text}</CourseName>
      </CourseSuggestion>
    </SuggestionInfoHover>
    
  ));

  return <Container>{options}</Container>;
}

export { CourseSuggestions };
