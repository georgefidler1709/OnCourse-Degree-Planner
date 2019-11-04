import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { DragDropContext } from 'react-beautiful-dnd';
import Term from './Term';

const Container = styled.div`
  display: flex;
`;

class Timeline extends Component {

  constructor(props) {
    super(props)
    this.state = this.preparePlan(props.location.state.plan)
  }

  preparePlan(plan) {
    let years = {}
    plan.enrollments.forEach((term) => {
      let curYear =  term.term.year
      let curTerm = term.term.term
      if(!(curYear in years)) {
        years[curYear] = {}
      }

      years[curYear][curTerm] = term.courses 
    })

    return years
  }

  onDragEnd = result => {
    // TODO: preserve reorder of terms
  };

  render() {
    return (
      <DragDropContext onDragEnd={this.onDragEnd}>
        {Object.keys(this.state).map(yearId => {
          const year = this.state[yearId];
          return (
            <Container>
              {Object.keys(year).map(termId => {
                const courses = year[termId];
                const termTag = "T" + termId.toString() + " " + yearId.toString()
                return <Term key={termTag} termId={termTag} courses={courses} />;
              })}
            </Container>
          )
        })}
      </DragDropContext>
    );
  }
}

export default Timeline
