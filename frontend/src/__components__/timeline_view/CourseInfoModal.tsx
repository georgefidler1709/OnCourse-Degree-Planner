import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

const year = '2020'
const handbook = `https://www.handbook.unsw.edu.au/undergraduate/courses/${year}`


interface CourseInfoModalProps {
  index: number;
  onHide: () => void;
  removeCourse: (s: string) => void; 
  show: boolean;
  code: string;
  name: string;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
}

function displayCourseReqs(reqs: string, req_type: string) {

  const noBullet = {
    "list-style-type" : "none",
  } as React.CSSProperties;
  
  return (
    <div id={req_type}>
      <h5>{req_type + ":"}</h5>
      {reqs ? (
        <ul>
          {reqs.split("\n").map(req => <li key={req}>{addLinks(req)}</li>)}
        </ul>
      ) : (
        <ul style={noBullet}>
          <li>None</li>
        </ul>
      )} 
    </div>
  )
}

function addLinks(req: string) {
  req = req.replace(/[()]/g, '');
  return req.split(' ').map(word => {
    if(word === "OR" || word === "AND" || word === "") return " " + word + " "
    return (<a key={word} href={`${handbook}/${word}`}>{word}</a>)
  })
}

function CourseInfoModal(props: CourseInfoModalProps) {
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {props.code + " - "}
            {props.name}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {displayCourseReqs(props.prereqs, "Prereqs")}
          {displayCourseReqs(props.coreqs, "Coreqs")}
          {displayCourseReqs(props.equivalents, "Equivalents")}
          {displayCourseReqs(props.exclusions, "Exclusions")}
          <hr/>
          <a href={`${handbook}/${props.code}`}>More Info</a>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>Close</Button>
          <Button variant="danger" onClick={() => {
            props.onHide()
            props.removeCourse(props.code)
          }}>Remove</Button>
        </Modal.Footer>
      </Modal>
    );
  }

  export default CourseInfoModal
