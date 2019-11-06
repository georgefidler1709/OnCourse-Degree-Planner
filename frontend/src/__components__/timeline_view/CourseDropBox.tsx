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
const Title = styled.h3`
  padding: 8px;
`;
const CourseList = styled.div`
  padding: 8px;
  flex-grow: 1;
  min-height: 100px;
`;

function CourseDropBox() {
  return (
    <Container>
      <Title>Remove</Title>
      <Droppable droppableId="Remove">
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
