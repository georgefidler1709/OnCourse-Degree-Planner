/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * Course.tsx
 * Component representing a course that may be dragged around and placed in boxes
 */

import React from 'react';
import styled from 'styled-components';
import { Draggable } from 'react-beautiful-dnd';
import CourseInfoModal from "./CourseInfoModal"
import { CourseReq } from '../../Api';

interface DraggableProps {
  isDragging: boolean;
  hasError: boolean;
  hasWarning: boolean;
}


const Container = styled.div<DraggableProps>`
  color: black;
  border: 2px solid lightgrey;
  border-radius: 6px;
  padding: 8px;
  margin-bottom: 8px;
  background-color: ${props => { 
    if (props.isDragging) return 'lightblue';
    else if(props.hasError) return 'red';
    else if(props.hasWarning) return 'yellow';
    else return 'white';
  }};

  &:hover {
    background-color: ${props => { 
      if (props.isDragging) return 'lightblue';
      else if(props.hasError) return 'darkred';
      else if(props.hasWarning) return 'darkyellow';
      else return 'grey';
    }};
  }
`;

interface CourseProps {
  key: string;
  index: number;
  code: string;
  name: string;
  units: number;
  prereqs: string;
  coreqs: string;
  equivalents: string;
  exclusions: string;
  removeCourse: (s : string) => void;
  error?: Array<CourseReq>;
  warn?: Array<string>;
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
            ref={provided.innerRef}
            isDragging={snapshot.isDragging}
            onClick={() => setModalShow(true)}
            hasError={props.error !== undefined}
            hasWarning={props.warn !== undefined}
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
