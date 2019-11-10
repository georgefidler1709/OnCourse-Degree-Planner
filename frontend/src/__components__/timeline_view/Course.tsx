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

interface CourseProps {
  key: string;
  index: number;
  code: string;
  name: string;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
}

function Course(props: CourseProps) {
    const [modalShow, setModalShow] = React.useState(false);
    console.log(props)
    return (
      <div>
      <Draggable draggableId={props.code} index={props.index}>
        {provided => (
          <Container
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            innerRef={provided.innerRef}
            onClick={() => setModalShow(true)}
          >
          {props.code}
          </Container>
        )}
      </Draggable>
        <CourseInfoModal
          {...props}
          show={modalShow}
          onHide={() => setModalShow(false)}
        />
      </div>
    );
}


export default Course
