import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

function CourseInfoModal(props) {
    const year = '2020'
    const handbook = `https://www.handbook.unsw.edu.au/undergraduate/courses/${year}`
    return (
      <Modal
        {...props}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title id="contained-modal-title-vcenter">
            {props.courseId}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <a href={`${handbook}/${props.courseId}`}>HERE</a>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }

  export default CourseInfoModal