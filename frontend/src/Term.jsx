import React, {Component} from 'react';
import styled from 'styled-components';
import { Droppable } from 'react-beautiful-dnd';
import Course from './Course';

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

class Term extends Component {
  render() {
    return (
      <Container>
        <Title>{this.props.termId}</Title>
        <Droppable droppableId={this.props.termId}>
          {provided => (
            <CourseList innerRef={provided.innerRef} {...provided.droppableProps}>
              {this.props.courses.map((course, index) => {
                const courseTag = `${course.subject.toString()}${course.code.toString()}`
                return <Course key={courseTag} courseId={courseTag} course={course} index={index} />
              }
                
              )}
              {provided.placeholder}
            </CourseList>
          )}
        </Droppable>
      </Container>
    );
  }
}

export default Term
