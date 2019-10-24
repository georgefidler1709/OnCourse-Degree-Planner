import React, {MouseEvent} from "react";
import Button from "react-bootstrap/Button";

import {Degree} from './Types'

function Suggestions(props: {degrees: Array<Degree>}) {
  const options = props.degrees.map((r,i) => (
    <div key={i}>
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
    </div>
  ));

  return <div>{options}</div>;
}

export default Suggestions;
