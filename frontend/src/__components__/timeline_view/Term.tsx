import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Course from './Course';
import { Course as ApiCourse } from '../../Api';

interface DroppableProps {
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
`;
const CourseList = styled.div<DroppableProps>`
  padding: 8px;
  flex-grow: 1;
  min-height: 100px;
  background-color: ${props => props.highlight ? 'lightgreen' : 'white'};
  transition: background-color 0.2 ease;
`;

interface TermProps {
  key: string;
  termId: string;
  courses: Array<ApiCourse>;
  highlight: boolean;
}

function Term(props: TermProps) {
  return (
    <Container>
      <Title>{"T" + props.termId}</Title>
      <Droppable droppableId={props.termId}>
        {provided => (
          <CourseList 
            innerRef={provided.innerRef} 
            {...provided.droppableProps}
            highlight={props.highlight}
          >
            {props.courses.map((course, index) => {
              let course_id = course.code.toString()
              return <Course 
                {...course}
                course_name={course.name}
                course_id={course_id}
                key={course_id} 
                index={index} />
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
