import React, {MouseEvent} from "react";
import Button from "react-bootstrap/Button";
import SuggestionInfoHover from "./SuggestionInfoHover"
import { useHistory } from "react-router-dom";
import {Position, SearchResult, CourseSearchResult} from '../../Types'


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
      <Button
        variant="light"
        className="suggestion"
        id={r.degree.id}
        value={r.degree.id}
        onClick={handleClick}
      >
        <h1 className="suggestion-code">{r.degree.id}</h1>
        <p className="suggestion-name">{r.text}</p>
      </Button>
    </SuggestionInfoHover>
    
  ));

  return <div className="suggestion-container">{options}</div>;
}

export default Suggestions;
export { Suggestions };

// interface CourseSuggestionsProps {
//   courses: Array<CourseSearchResult>;
//   add_event(course: Course): any;
// }

function CourseSuggestions(props: {courses: Array<CourseSearchResult>, add_event(course: Course): Function}) {

  const year : string = "2020"
  const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/courses/${year}/`
  const placement : Position = "right"
  let history = useHistory();
  
  const options = props.courses.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.course.code}>More Info</a>
      }
      placement={placement}
      delay={200}
      key={r.course.code}
    >
      <Button
        variant="light"
        className="suggestion"
        id={r.course.code}
        value={r.course.code}
        onClick={() => props.add_event(r.course)}
      >
        <h1 className="suggestion-code">{r.code}</h1>
        <p className="suggestion-name">{r.text}</p>
      </Button>
    </SuggestionInfoHover>
    
  ));

  return <div className="suggestion-container">{options}</div>;
}

export { CourseSuggestions };