import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { DragDropContext, DropResult } from 'react-beautiful-dnd';
import Term from './Term';
import { RouteComponentProps } from 'react-router-dom';
import { GeneratorResponse, YearPlan, TermPlan } from '../../Api';

const Container = styled.div`
  display: flex;
`;

interface TimelineState extends GeneratorResponse { }

class Timeline extends Component<RouteComponentProps, TimelineState> {

  constructor(props: RouteComponentProps) {
    super(props)
    this.state = props.location.state.plan
  }

  onDragEnd = (result: DropResult) => {
    // TODO: preserve reorder of terms
  };

  getCourseInfo(course_id: string) {
    return this.state.courses.find((course) => course.subject + course.code.toString() === course_id)!
    
  }

  render() {
    const program = this.state.program

    // fill in required years for the program duration
    let timeline = []
    let year = program.enrollments[0].year
    for(let i = 0; i < program.duration; ++i) {
      timeline.push(year++)
    }

    return (
      <DragDropContext onDragEnd={this.onDragEnd}>
        {timeline.map((year_num, year_index) => {
          let year: YearPlan  = {term_plans: [], year: year_num}
          if(year_index < program.enrollments.length) {
            year = program.enrollments[year_index]
          } 

          // fill in the minimum 3 terms per year
          const required_terms = [1,2,3]
          let cur_term = 0
          let terms : Array<TermPlan> = []

          // fills in terms such that 'required terms' are always present and always in order
          // but other terms can be inserted in between
          year.term_plans.forEach(term => {
            let new_term = required_terms.findIndex(req => req === term.term)
            if(new_term > cur_term) {
              for( ; cur_term < new_term; ++cur_term) terms.push({course_ids: [], term: required_terms[cur_term]})
            } 
            if(new_term === cur_term) ++cur_term
            terms.push(term)
          })

          // if any 'required terms' were missing from the end, add them on here
          for( ; cur_term < required_terms.length; ++cur_term) terms.push({course_ids: [], term: required_terms[cur_term]})

          return (
            <Container key={year_num}>
              {terms.map(term => {
                const courses = term.course_ids.map(course_id => this.getCourseInfo(course_id));
                const term_tag = "T" + term.term.toString() + " " + year_num.toString()
                return <Term key={term_tag} termId={term_tag} courses={courses} />;
              })}
            </Container>
          )
        })}
      </DragDropContext>
    );
  }
}

export default Timeline
