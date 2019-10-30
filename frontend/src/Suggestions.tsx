import React, {MouseEvent} from "react";
import Button from "react-bootstrap/Button";
import SuggestionInfoHover from "./SuggestionInfoHover"

import {Degree} from './Types'

const year : string = "2020"
const handbook : string = `https://www.handbook.unsw.edu.au/undergraduate/specialisations/${year}/`
const placement : string = "right"

function Suggestions(props: {degrees: Array<Degree>}) {
  const options = props.degrees.map((r,i) => (
    <SuggestionInfoHover
      content={
        <a href={handbook + r.code}>More Info</a>
      }
      placement={placement}
      delay={200}
    >
      <Button
        variant="light"
        className="suggestion"
        id={r.id.toString()}
        value={r.name}
        onClick={(event: MouseEvent<HTMLButtonElement>) => console.log(event.currentTarget.value)}
      >
        <h1 className="suggestion-code">{r.code}</h1>
        <p className="suggestion-name">{r.name}</p>
      </Button>
      <br />
    </SuggestionInfoHover>
  ));

  return <div>{options}</div>;
}

export default Suggestions;
