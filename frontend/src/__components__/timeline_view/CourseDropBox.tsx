import React from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import { Course as ApiCourse } from "../../Api";
import Course from './Course';

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
  add_course: ApiCourse;
  remove_course: (id: string) => void;
}

function CourseDropBox(props: DropBoxProps) {

  if (props.add_course !== undefined) {
    // make a course and put it in the box
    return (
      <Container>
        <Title>{props.type}</Title>
        <Droppable droppableId={props.type}>
          {provided => (
            <CourseList innerRef={provided.innerRef} {...provided.droppableProps}>
              <Course
                {...props.add_course}
                key={props.add_course.code}
                index={0}
                removeCourse={props.remove_course}
              />
            </CourseList>
          )}
        </Droppable>
      </Container>
    );
  } else {
    // placeholder box
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

}

export default CourseDropBox
