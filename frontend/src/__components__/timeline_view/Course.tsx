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
  index: number;
  code: string;
  name: string;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
  removeCourse: (s : string) => void;
}

function Course(props: CourseProps) {
    const [modalShow, setModalShow] = React.useState(false);
    return (
      <div>
      <Draggable draggableId={props.code} index={props.index}>
        {(provided, snapshot) => (
          <Container
            {...provided.draggableProps}
            {...provided.dragHandleProps}
            innerRef={provided.innerRef}
            isDragging={snapshot.isDragging}
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
