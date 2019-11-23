/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * CourseInfoModal.tsx
 * Component that pops up when a course is clicked. Displays course information and outstanding requirements
 * and warnings
 */

import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import { CourseReq } from '../../Api';
import { SubTitle } from '../../Types';
import { COURSE_HANDBOOK_PREFIX } from '../../Constants'
import styled from 'styled-components';

const UOC = styled.h5`
  margin-bottom: 16px;
`

interface CourseInfoModalProps {
  index: number;
  onHide: () => void;
  removeCourse: (s: string) => void; 
  show: boolean;
  code: string;
  name: string;
  units: number;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
  error?: Array<CourseReq>;
  warn?: Array<string>;
}

/**
 * converts a requirement string sent from the backend into a bulleted list
 */
function displayCourseReqs(reqs: string, req_type: string) {
  const noBullet = {
    "listStyleType" : "none",
  } as React.CSSProperties;
  
  return (
    <div id={req_type}>
      <h5>{req_type + ":"}</h5>
      {reqs ? (
        <ul>
          {reqs.split("\n").map((req,index) => <li key={index}> {addLinks(req)}</li>)}
        </ul>
      ) : (
        <ul style={noBullet} key={"none"}>
          <li>None</li>
        </ul>
      )} 
    </div>
  )
}

/**
 * parses a requirement string and adds relevant links
 */
function addLinks(req: string) {
  const re = new RegExp('^[A-Z]{4}[0-9]{4}$');
  req = req.replace(/[()]/g, '');
  return req.split(' ').map(word => {
    if(!word.match(re)) return " " + word + " "
    return (<a 
              key={word}
              href={`${COURSE_HANDBOOK_PREFIX}${word}`}
              target="_blank"
              rel="noopener noreferrer" 
              >{word}
            </a>
            )
  })
}

/**
 * component representing an outstanding requirement
 */
function Requirement(props: {filter_type: string, info: Array<string>}) {
  return (
    <div key={props.filter_type}>
      <p>{props.filter_type}</p>
    <ul>
    {props.info.map(info => <li key={info}>{`${info}`}</li>)}
    </ul>
  </div>);
}

/**
 * component representing all outstanding requirements of a course
 */
function Requirements(props: {title: string,  degree_reqs: Array<CourseReq>}) {
  return (<>
  <SubTitle>{props.title}</SubTitle>
    {props.degree_reqs.map(req => { return (
      <Requirement 
        key={req.filter_type} 
        info={req.info} 
        filter_type={`${req.filter_type} violation(s)`}/>
    )})}
    </>);
}

/**
 * component that pops up when a course is clicked, showing all course information
 */
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
        <UOC>UOC: {props.units}</UOC>
        {displayCourseReqs(props.prereqs, "Prereqs")}
        {displayCourseReqs(props.coreqs, "Coreqs")}
        {displayCourseReqs(props.equivalents, "Equivalents")}
        {displayCourseReqs(props.exclusions, "Exclusions")}
        <hr/>
        <a href={`${COURSE_HANDBOOK_PREFIX}${props.code}`}>More Info</a>
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
