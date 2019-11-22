import React from 'react';
import styled from 'styled-components';
import { StyledComponent } from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import { Course as ApiCourse, CourseReq } from '../../Api';
import Course from './Course';

type DivComponent = StyledComponent<"div", any>;
type TitleComponent = StyledComponent<"h5", any>;

interface DroppableProps {
  isDraggingOver: boolean;
  highlight: boolean;
  termWarning: boolean;
}

const CourseList = styled.div<DroppableProps>`
  padding: 8px;
  flex-grow: 1;
  min-height: 100px;
  transition: background-color 0.2s ease;
  background-color: ${props => {
    if(props.highlight) {
      return props.isDraggingOver ? 'green' : 'lightgreen'
    } else if (props.termWarning) {
		return props.isDraggingOver ? 'yellow' : 'lightyellow'
	} else {
		return props.isDraggingOver ? 'lightgrey' : '#ededed'
	}
  }};
`;

interface DropboxProps {
  name: string;
  id: string;
  courses: Array<ApiCourse>;
  highlight: boolean;
  termWarning: boolean;
  removeCourse: (s: string) => void;
  getError?: (s: string) => (Array<CourseReq> | undefined);
  getWarn?: (s: string) => (Array<string> | undefined);
}

function CourseDropBox(Container: DivComponent, Title: TitleComponent) {
  return (props: DropboxProps) => (
    <Container>
      <Title>{props.name}</Title>
      <Droppable droppableId={props.id}>
        {(provided, snapshot) => (
          <CourseList 
            ref={provided.innerRef} 
            {...provided.droppableProps}
            isDraggingOver={snapshot.isDraggingOver}
            highlight={props.highlight}
            termWarning={props.termWarning}
          >
            {props.courses.map((course, index) => {
              let course_id = course.code.toString()
              return <Course 
                {...course}
                key={course_id} 
                index={index} 
                removeCourse={props.removeCourse}
                error={props.getError === undefined ? undefined : props.getError(course_id)}
                warn={props.getWarn === undefined ? undefined : props.getWarn(course_id)}
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


export default CourseDropBox
