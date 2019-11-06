import React from "react";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";

interface CourseInfoModalProps {
  index: number;
  onHide: () => void;
  show: boolean;
  course_id: string;
  course_name: String;
}

function CourseInfoModal(props: CourseInfoModalProps) {
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
            {props.course_id + " - "}
            {props.course_name}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <a href={`${handbook}/${props.course_id}`}>More Info</a>
        </Modal.Body>
        <Modal.Footer>
          <Button onClick={props.onHide}>Close</Button>
        </Modal.Footer>
      </Modal>
    );
  }

  export default CourseInfoModal
