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
        <Title>{this.props.term_id}</Title>
        <Droppable droppableId={this.props.term_id}>
          {provided => (
            <CourseList innerRef={provided.innerRef} {...provided.droppableProps}>
              {this.props.courses.map((course, index) => {
                return <Course key={course.course_id} course_id={course.course_id} course={course.course_info} index={index} />
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
