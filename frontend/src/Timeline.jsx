import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { DragDropContext } from 'react-beautiful-dnd';
import mockDegree from './mockDegree';
import Term from './Term';

const Container = styled.div`
  display: flex;
`;

class Timeline extends Component {
  constructor(props) {
    //console.log(props.location.state.plan)
    super(props)
    this.state = mockDegree //props.location.state.plan
  }

  onDragEnd = result => {
    // TODO: preserve reorder of terms
  };

  render() {
    return (
      <DragDropContext onDragEnd={this.onDragEnd}>
        {this.state.yearOrder.map(yearId => {
          const year = this.state.years[yearId];

          return (
            <Container>
              {year.termOrder.map(termId => {
                const term = this.state.terms[termId];
                const courses = term.courseIds.map(courseId => this.state.courses[courseId]);
      
                return <Term key={term.id} term={term} courses={courses} />;
              })}
            </Container>
          )
        })}
      </DragDropContext>
    );
  }
}

export default Timeline
