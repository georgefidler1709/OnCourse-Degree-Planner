import React from "react";
import Button from "react-bootstrap/Button";

function Suggestions(props) {
  const options = props.degrees.map((r,i) => (
    <div key={i}>
      <Button
        variant="light"
        className="suggestion"
        id={r.id}
        value={r.name}
        onClick={event => console.log(event.target.value)}
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
