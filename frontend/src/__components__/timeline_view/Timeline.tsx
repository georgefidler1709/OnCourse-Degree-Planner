import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { DragDropContext, DropResult, DragStart } from 'react-beautiful-dnd';
import Term from './Term';
import { RouteComponentProps } from 'react-router-dom';
import { GeneratorResponse, YearPlan, TermPlan} from '../../Api';
import {API_ADDRESS} from '../../Constants'
import { Navbar, Nav, Button } from 'react-bootstrap'
import InfoBar from "./InfoBar"
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'

const TimeLineContext = styled.div`
  display: flex;
  justify-content: center;
`;
const Container = styled.div`
  display: flex;
`;

const LColumn = styled.div`
  float: left;
  width: 70%;
  padding: 10px;
  min-height: 500px;
`;

const RColumn = styled.div`
  float: left;
  width: 30%;
  padding: 10px;
  min-height: 500px;
`;

const NavButton = styled(Button)`
  margin-left: 8px;
  margin-right: 8px;
`;

interface TimelineState extends GeneratorResponse { }

class Timeline extends Component<RouteComponentProps<{degree: string}>, TimelineState> {

  constructor(props: RouteComponentProps<{degree: string}>) {
    super(props)
    let code = props.match.params["degree"]
    fetch(API_ADDRESS + `/${code}/gen_program.json`)
    .then(response => response.json())
    .then(plan => {
      this.setState(plan) 
      this.addMissingTerms()
    })
  }

  addMissingTerms() {
    const program = this.state.program
    // fill in required years for the program duration
    let timeline: Array<number> = []
    let year_max: number = program.enrollments[0].year
    for(let i = 0; i < program.duration; ++i) {
      timeline.push(year_max++)
    }

    timeline.forEach((year_num, year_index) => {
      if(year_index >= program.enrollments.length) this.addYear(year_num)
      let year = program.enrollments[year_index]
        // fill in the minimum 3 terms per year
      const required_terms = [1,2,3]
      let cur_term = 0
      // fills in terms such that 'required terms' are always present and always in order
      // but other terms can be inserted in between
      console.log(year.year)
      year.term_plans.forEach(term => {
        let new_term = required_terms.findIndex(req => req === term.term)
        if(new_term > cur_term) {
          for( ; cur_term < new_term; ++cur_term) this.addTerm(cur_term + 1, year, year_index);
        } 
        if(new_term !== -1) cur_term++ 
      })
      // if any 'required terms' were missing from the end, add them on here
      for( ; cur_term < required_terms.length; ++cur_term) this.addTerm(cur_term + 1, year, year_index);
    })

    console.log(this.state)
  }


  addTerm(newTermId: number, year: YearPlan, yearIdx: number) {
    let idx = year.term_plans.findIndex(term => term.term > newTermId)
    if(idx === -1) {
      year.term_plans.push({course_ids: [], term: newTermId, highlight: false})
      idx = year.term_plans.length - 1
    }
    else year.term_plans.splice(idx, 0, {course_ids: [], term: newTermId, highlight: false})

    let newState = {
      ...this.state,
    }
    newState.program.enrollments[yearIdx] = year
    this.setState(newState)
    return idx
  }

  addYear(newYearId: number) {
    let newState = {
      ...this.state,
    }

    let idx = newState.program.enrollments.findIndex(year => year.year > newYearId)
    if(idx === -1) {
      newState.program.enrollments.push({term_plans: [], year: newYearId})
      idx = newState.program.enrollments.length - 1
    }
    else newState.program.enrollments.splice(idx, 0, {term_plans: [], year: newYearId})

    this.setState(newState)

    return idx
  }

  removeCourse(sourceIdx: number, draggableId: string, startTermId: number, startYearId: number) {
    let startYearIdx = this.state.program.enrollments.findIndex(year => year.year === startYearId)
    let startYear = this.state.program.enrollments[startYearIdx]
    let startTermIdx = startYear.term_plans.findIndex(term => term.term === startTermId)
    let startTerm = startYear.term_plans[startTermIdx]

    const newCourseIds = Array.from(startTerm.course_ids)
      newCourseIds.splice(sourceIdx, 1)

      const newTerm = {
        ...startTerm,
        course_ids: newCourseIds
      }

      let newYear = {
        ...startYear,
      }

      newYear.term_plans[startTermIdx] = newTerm

      let newCourses = this.state.courses
      delete newCourses['draggableId']

      let newState = {
        ...this.state,
      }

      newState.courses = newCourses
      newState.program.enrollments[startYearIdx] = newYear

      this.setState(newState)
      
      
  }

  onDragEnd = (result: DropResult) => {

    const { destination, source, draggableId } = result

    // if not dragged into a term, don't change state
    if(!destination) {
      this.resetTermHighlights()
      return;
    }
    // if location not changed, don't change state
    if(destination.droppableId === source.droppableId &&
      destination.index === source.index) {
      this.resetTermHighlights()
      return;
    }

    // get year and term for the start and dest of a drag
    let [startTermId, startYearId] = source.droppableId.split(" ").map(s => parseInt(s))
    if(destination.droppableId === "Remove") {
      this.removeCourse(source.index, draggableId, startTermId, startYearId)
      this.resetTermHighlights()
      return
    }
    let [destTermId, destYearId] = destination.droppableId.split(" ").map(s => parseInt(s))

    let destYearIdx = this.state.program.enrollments.findIndex(year => year.year === destYearId)
    // if destination year does not exist in state (i.e. it's empty), add it
    let destYear = this.state.program.enrollments[destYearIdx]

    let startYearIdx = destYearIdx
    let startYear = destYear
    if(startYearId !== destYearId) {
      startYearIdx = this.state.program.enrollments.findIndex(year => year.year === startYearId)
      startYear = this.state.program.enrollments[startYearIdx]
    }

    let destTermIdx = destYear.term_plans.findIndex(term => term.term === destTermId)
    // if destination term does not exist in state (i.e. it's empty), add it
    let destTerm = destYear.term_plans[destTermIdx]

    let startTermIdx = destTermIdx
    let startTerm = destTerm
    if(startYearId !== destYearId || startTermId !== destTermId) {
      startTermIdx = startYear.term_plans.findIndex(term => term.term === startTermId)
      startTerm = startYear.term_plans[startTermIdx]
    }

    let newState = {
      ...this.state,
    }

    // inter-year drag
    if(startYearId !== destYearId) {
      const startCourseIds = Array.from(startTerm.course_ids)
      startCourseIds.splice(source.index, 1)
  
      const newStartTerm = {
        ...startTerm,
        course_ids: startCourseIds
      }
  
      let newStartYear = {
        ...startYear
      }
      newStartYear.term_plans[startTermIdx] = newStartTerm
  
      const destCourseIds = Array.from(destTerm.course_ids)
      destCourseIds.splice(destination.index, 0, draggableId)
  
      const newDestTerm = {
        ...destTerm,
        course_ids: destCourseIds
      }
  
      let newDestYear = {
        ...destYear
      }
      newDestYear.term_plans[destTermIdx] = newDestTerm
  
      newState.program.enrollments[startYearIdx] = newStartYear;
      newState.program.enrollments[destYearIdx] = newDestYear;
    }
    // inter-term drag
    else if(startTermId !== destTermId) {
      const startCourseIds = Array.from(startTerm.course_ids)
      startCourseIds.splice(source.index, 1)
  
      const newStartTerm = {
        ...startTerm,
        course_ids: startCourseIds
      }

      const destCourseIds = Array.from(destTerm.course_ids)
      destCourseIds.splice(destination.index, 0, draggableId)

      const newDestTerm = {
        ...destTerm,
        course_ids: destCourseIds
      }
  
      let newYear = {
        ...startYear
      }

      newYear.term_plans[startTermIdx] = newStartTerm
      newYear.term_plans[destTermIdx] = newDestTerm

      newState.program.enrollments[startYearIdx] = newYear
    } 
    // drag within a single term
    else {
      const newCourseIds = Array.from(startTerm.course_ids)
      newCourseIds.splice(source.index, 1)
      newCourseIds.splice(destination.index, 0, draggableId)

      const newTerm = {
        ...startTerm,
        course_ids: newCourseIds
      }

      let newYear = {
        ...startYear,
      }
      newYear.term_plans[startTermIdx] = newTerm
      newState.program.enrollments[startYearIdx] = newYear;
    }
    this.setState(newState)
    this.resetTermHighlights()
  };

  getCourseInfo(course_id: string) {
    return this.state.courses[course_id]!
  }

  resetTermHighlights() {
    let newEnrollments = this.state.program.enrollments.map(year => {
      let newYear = {
        ...year,
      }
      newYear.term_plans = year.term_plans.map(term => {
        let newTerm = {...term}
        newTerm.highlight = false
        return newTerm
      })

      return newYear
    })

    let newState = {
      ...this.state,
      program: {
        ...this.state.program,
        enrollments: newEnrollments
      }
    }
    this.setState(newState)
  }

  isCourseOffered(courseId: string, term: TermPlan, year: YearPlan) {
    const termsOffered = this.state.courses[courseId].terms
    const isOffered = termsOffered.findIndex(offering => 
      offering.term === term.term && offering.year === year.year
    )
    return isOffered !== -1
  }

  onDragStart = (start: DragStart) => {
    const { draggableId } = start

    let newEnrollments = this.state.program.enrollments.map(year => {
      let newYear = {
        ...year,
      }
      newYear.term_plans = year.term_plans.map(term => {
        let newTerm = {...term}
        newTerm.highlight = this.isCourseOffered(draggableId, term, year)
        return newTerm
      })

      return newYear
    })

    let newState = {
      ...this.state,
      program: {
        ...this.state.program,
        enrollments: newEnrollments
      }
    }

    this.setState(newState)
  }

  savePlan() {
    html2canvas(document.getElementById('timeline')!).then(function(canvas) {
      canvas.toBlob(function(blob) {
        // Generate file download
        saveAs(blob!, "plan.png");
    });
  });
  }

  
  render() {
    if(!this.state) return <div></div>

    const program = this.state.program

    return (
      <div>
        <Navbar bg="dark" variant="dark" id="navbar">
          <Navbar.Brand href="#home">OnCourse</Navbar.Brand>
          <Nav className="mr-auto">
          </Nav>
          <NavButton variant="outline-info" onClick={this.savePlan}><i className="fa fa-save"></i></NavButton>
          <NavButton variant="outline-info"><i className="fa fa-cog"></i></NavButton>
        </Navbar>
        <br />
          <TimeLineContext>
            <DragDropContext 
              onDragEnd={this.onDragEnd}
              onDragStart={this.onDragStart}
            >
              { 
                <div>
                  <LColumn id="timeline"> {
                    program.enrollments.map(year => (
                        <div>
                            <Container key={year.year}>
                              {year.term_plans.map(term => {
                                const courses = term.course_ids.map(course_id => this.getCourseInfo(course_id));
                                const term_tag = term.term.toString() + " " + year.year.toString()
                                return <Term key={term_tag} termId={term_tag} courses={courses} highlight={term.highlight}/>;
                              })}
                            </Container>
                        </div>
                      )
                    )
                  } </LColumn> 
                  <RColumn>
                    <InfoBar 
                      degree_id={this.state.program.id}
                      degree_name={this.state.program.name}
                      degree_reqs={this.state.program.reqs}
                    />
                  </RColumn>
                </div>
              }  
            </DragDropContext>
          </TimeLineContext>
        </div>
    );
  }
}

export default Timeline
