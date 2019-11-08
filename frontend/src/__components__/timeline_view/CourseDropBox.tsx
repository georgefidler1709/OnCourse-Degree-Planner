import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';

const Container = styled.div`
  margin: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 220px;

  display: flex;
  flex-direction: column;
`;
const Title = styled.h5`
  padding: 8px;
`;
const CourseList = styled.div`
  padding: 8px;
  flex-grow: 1;
  min-height: 50px;
`;

interface DropBoxProps {
  type: string;
}

function CourseDropBox(props: DropBoxProps) {
  return (
    <Container>
      <Title>{props.type}</Title>
      <Droppable droppableId={props.type}>
        {provided => (
          <CourseList innerRef={provided.innerRef} {...provided.droppableProps}>
            {provided.placeholder}
          </CourseList>
        )}
      </Droppable>
    </Container>
  );
}

export default CourseDropBox
