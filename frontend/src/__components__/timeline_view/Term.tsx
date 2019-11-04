import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Course from './Course';
import { Course as ApiCourse } from '../../Api';

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

interface TermProps {
  key: string;
  termId: string;
  courses: Array<ApiCourse>;
}

function Term(props: TermProps) {
  return (
    <Container>
      <Title>{props.termId}</Title>
      <Droppable droppableId={props.termId}>
        {provided => (
          <CourseList innerRef={provided.innerRef} {...provided.droppableProps}>
            {props.courses.map((course, index) => {
              let course_id = course.subject + course.code.toString()
              return <Course 
                {...course}
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
