import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Course from './Course';
import { Course as ApiCourse } from '../../Api';

interface DroppableProps {
  isDraggingOver: boolean;
  highlight: boolean;
}

const Container = styled.div`
  margin-top: 8px;
  margin-bottom: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 400px;
  text-align: center;
  display: flex;
  flex-direction: column;
`;
const Title = styled.h3`
  padding: 8px;
  font-family: Arial, Helvetica, sans-serif;
  border-bottom: 1px solid lightgrey;
  margin: 0px;
`;
const CourseList = styled.div<DroppableProps>`
  padding: 8px;
  flex-grow: 1;
  min-height: 100px;
  transition: background-color 0.2s ease;
  background-color: ${props => {
    if(props.highlight) {
      return props.isDraggingOver ? 'green' : 'lightgreen'
    } else return props.isDraggingOver ? 'lightgrey' : '#ededed'
  }};
`;

interface TermProps {
  key: string;
  termId: string;
  courses: Array<ApiCourse>;
  highlight: boolean;
  removeCourse: (s: string) => void;
}

function Term(props: TermProps) {
  return (
    <Container>
      <Title>{"T" + props.termId}</Title>
      <Droppable droppableId={props.termId}>
        {(provided, snapshot) => (
          <CourseList 
            ref={provided.innerRef} 
            {...provided.droppableProps}
            isDraggingOver={snapshot.isDraggingOver}
            highlight={props.highlight}
          >
            {props.courses.map((course, index) => {
              let course_id = course.code.toString()
              return <Course 
                {...course}
                key={course_id} 
                index={index} 
                removeCourse={props.removeCourse}
                />
            }
            )}
            {provided.placeholder}
          </CourseList>
        )}
      </Droppable>
    </Container>
  );
}

export default Term
