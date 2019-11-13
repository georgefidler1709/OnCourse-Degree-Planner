import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';
import CourseInfoModal from "./CourseInfoModal"

interface DraggableProps {
  isDragging: boolean;
  error?: string;
}


const Container = styled.div<DraggableProps>`
  border: 1px solid lightgrey;
  border-radius: 2px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: ${props => { 
    if (props.isDragging) return 'lightblue';
    else if(props.error !== undefined) return 'red';
    else return 'white';
  }};

  &:hover {
    background-color: ${props => { 
      if (props.isDragging) return 'lightblue';
      else if(props.error !== undefined) return 'darkred';
      else return 'grey';
    }};
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
  error?: string;
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
            error={props.error}
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
