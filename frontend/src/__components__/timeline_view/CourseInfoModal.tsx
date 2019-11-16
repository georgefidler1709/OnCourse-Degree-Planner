import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import { CourseReq } from '../../Api';
import { SubTitle } from '../../Types';

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
  error?: Array<CourseReq>;
  warn?: Array<string>;
}

function displayCourseReqs(reqs: string, req_type: string) {

  const noBullet = {
    "listStyleType" : "none",
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

function Requirements(props: {title: string, heading: (x: string) => string, degree_reqs: Array<CourseReq>}) {
  return (<>
  <SubTitle>{props.title}</SubTitle>
    {props.degree_reqs.map(req => { return (
      <div key={req.filter_type}>
        <p>{props.heading(req.filter_type)}</p>
      <ul>
        {req.info.map(info => <li key={info}>{`${info}`}</li>)}
      </ul>
    </div>
    )
    })}
    </>);
}

function CourseInfoModal(props: CourseInfoModalProps) {
    return (
      <Modal
        show={props.show}
        onHide={props.onHide}
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
          {props.error !== undefined && 
            <span style={{color:"red"}}>
              <Requirements
                title="Errors"
                heading={(filter) => `${filter} violation(s)`}
                degree_reqs={props.error}/>
            </span> }
          {props.warn !== undefined && 
            <span style={{color:"yellow"}}>
              <Requirements
                title="Warnings"
                degree_reqs={[{filter_type: "Warning(s)", info: props.warn}]}
                heading={(x)=>x}
              />
            </span> }
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
