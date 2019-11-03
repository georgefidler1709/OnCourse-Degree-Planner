import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';
import CourseInfoModal from "./CourseInfoModal"

const Container = styled.div`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: white;
`;

function Course(props) {
    const [modalShow, setModalShow] = React.useState(false);
    return (
      <div>
      <Draggable draggableId={props.courseId} index={props.index}>
        {provided => (
          <Container
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            innerRef={provided.innerRef}
            onClick={() => setModalShow(true)}
          >
            {props.courseId}
          </Container>
        )}
      </Draggable>
        <CourseInfoModal
          show={modalShow}
          onHide={() => setModalShow(false)}
          courseId={props.courseId}
          course={props.course}
        />
      </div>
    );
}


export default Course
