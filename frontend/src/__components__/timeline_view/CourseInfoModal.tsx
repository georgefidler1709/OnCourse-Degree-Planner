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
          {reqs.split("\n").map((req,index) => <li key={index}>{addLinks(req)}</li>)}
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
  const re = new RegExp('^[A-Z]{4}[0-9]{4}$');
  req = req.replace(/[()]/g, '');
  return req.split(' ').map(word => {
    if(!word.match(re)) return " " + word + " "
    return (<a key={word} href={`${handbook}/${word}`}>{word}</a>)
  })
}

function Requirement(props: {filter_type: string, info: Array<string>}) {
  return (
    <div key={props.filter_type}>
      <p>{props.filter_type}</p>
    <ul>
    {props.info.map(info => <li key={info}>{`${info}`}</li>)}
    </ul>
  </div>);
}

function Requirements(props: {title: string,  degree_reqs: Array<CourseReq>}) {
  return (<>
  <SubTitle>{props.title}</SubTitle>
    {props.degree_reqs.map(req => { return (<Requirement info={req.info} filter_type={`${req.filter_type} violation(s)`}/>)})}
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
                degree_reqs={props.error}/>
            </span> }
          {props.warn !== undefined && 
              <Requirement
                filter_type="Warning(s)"
                info={props.warn}
              />}
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
