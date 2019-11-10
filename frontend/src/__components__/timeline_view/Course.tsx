import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';
import CourseInfoModal from "./CourseInfoModal"

interface DraggableProps {
  isDragging: boolean;
}


const Container = styled.div<DraggableProps>`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: ${props => props.isDragging ? 'lightblue' : 'white'};

  &:hover {
    background-color: ${props => props.isDragging ? 'lightblue' : 'lightgrey'};
  }
`;

interface CourseProps {
  key: string;
  course_id: string;
  index: number;
  course_name: String;
}

function Course(props: CourseProps) {
    const [modalShow, setModalShow] = React.useState(false);
    return (
      <div>
      <Draggable draggableId={props.course_id} index={props.index}>
        {(provided, snapshot) => (
          <Container
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            innerRef={provided.innerRef}
            isDragging={snapshot.isDragging}
            onClick={() => setModalShow(true)}
          >
          {props.course_id}
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
