import React, {MouseEvent} from "react";
import Button from "react-bootstrap/Button";
import SuggestionInfoHover from "./SuggestionInfoHover"

import {Position} from './Types'
import {SimpleDegrees} from './Api'

const year : string = "2020"
const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/specialisations/${year}/`
const placement : Position = "right"

function Suggestions(props: {degrees: SimpleDegrees}) {
  const options = props.degrees.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.id.toString()}>More Info</a>
      }
      placement={placement}
      delay={200}
      key={r.id}
    >
      <Button
        variant="light"
        className="suggestion"
        id={r.id.toString()}
        value={r.name}
        onClick={(event: MouseEvent<HTMLButtonElement>) => console.log(event.currentTarget.value)}
      >
        <h1 className="suggestion-code">{r.id}</h1>
        <p className="suggestion-name">{r.name}</p>
      </Button>
    </SuggestionInfoHover>
  ));

  return <div>{options}</div>;
}

export default Suggestions;
