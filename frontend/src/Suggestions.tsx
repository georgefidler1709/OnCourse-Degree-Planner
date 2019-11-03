import React, {MouseEvent} from "react";
import Button from "react-bootstrap/Button";
import SuggestionInfoHover from "./SuggestionInfoHover"
import { useHistory } from "react-router-dom";

import {Position} from './Types'
import {SimpleDegrees} from './Api'


function Suggestions(props: {degrees: SimpleDegrees}) {

  const year : string = "2020"
  const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/specialisations/${year}/`
  const placement : Position = "right"
  let history = useHistory();

  function handleClick(event: MouseEvent<HTMLButtonElement>) {
    history.push("/timeline")
  }

  const options = props.degrees.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.id}>More Info</a>
      }
      placement={placement}
      delay={200}
      key={r.id}
    >
      <Button
        variant="light"
        className="suggestion"
        id={r.id}
        value={r.name}
        onClick={handleClick}
      >
        <h1 className="suggestion-code">{r.id}</h1>
        <p className="suggestion-name">{r.name}</p>
      </Button>
    </SuggestionInfoHover>
    
  ));

  return <div>{options}</div>;
}

export default Suggestions;
