import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { DragDropContext, DropResult, DragStart } from 'react-beautiful-dnd';
import Term from './Term';
import { RouteComponentProps } from 'react-router-dom';
import { Course } from '../../Api';
import {API_ADDRESS} from '../../Constants'
import { Navbar, Nav, Button } from 'react-bootstrap'
import InfoBar from "./InfoBar"
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
import { TimelineState, YearState, TermState } from '../../Types'

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
`;

const RColumn = styled.div`
  float: left;
  width: 30%;
  padding: 10px;
`;

const NavButton = styled(Button)`
  margin: 0px 8px;
`;

const YearButton = styled(Button)`
  width: 40px;
  margin: 0px 4px;
`

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
      year.term_plans.forEach(term => {
        let new_term = required_terms.findIndex(req => req === term.term)
        if(new_term > cur_term) {
          for( ; cur_term < new_term; ++cur_term) this.addTerm(cur_term + 1, year, year_index);
        } 
        if(new_term !== -1) ++cur_term
      })
      // if any 'required terms' were missing from the end, add them on here
      for( ; cur_term < required_terms.length; ++cur_term) this.addTerm(cur_term + 1, year, year_index);
    })

    for(let year_max = this.state.program.enrollments.length; year_max > timeline.length; --year_max) {
      this.removeYear()
    }

    console.log(this.state)
  }

  isYearEmpty(year: YearState) {
    return year.term_plans.findIndex(term => term.course_ids.length > 0) === -1;
  }

  removeYear() {
    let newState = {
      ...this.state,
    }

    const enrollments = this.state.program.enrollments;
    if(this.isYearEmpty(enrollments[enrollments.length - 1])) newState.program.enrollments.pop()
    else {
      alert("Remove courses from a year before deleting it")
      newState.program.duration++
    }

    this.setState(newState)
  }

    // function to pass to CourseSuggestions in Suggestions.tsx via InfoBar's SearchCourse
  // sets this.state.add_course to be the Course passed in
  addCourse(course: Course) {
    let newState = {
      ...this.state,
    }

    newState.add_course = course

    this.setState(newState)

  }


  addTerm(newTermId: number, year: YearState, yearIdx: number) {
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

    // check if this increased program duration
    if (newState.program.enrollments.length > newState.program.duration) {
      newState.program.duration += 1
    }

    this.setState(newState)

    return idx
  }

  // takes the current program in state,
  // assuming it has been modified,
  // and updates it via an API call to /check_program.json
  updateProgram(state: TimelineState): void {
    // if you change anything other than the enrollments or the degree duration in front-end
    // go to server/degrees.py and change in check_program() what is being created as the new state
    // to reflect those changes

    var request = new Request(API_ADDRESS + '/check_program.json', {
      method: 'POST',
      body: JSON.stringify(this.state.program),
      headers: new Headers(/*{'Accept': 'application/json', 'Content-Type': 'application/json', 'dataType': 'json'}*/)
    });

    fetch(request)
    .then(response => response.json())
    .then(plan => {
      this.setState(plan)
    })
  }

  removeCourse(draggableId: string) {
    let sourceIdx = -1
    let startTermIdx = -1
    let startYearIdx = -1

    startYearIdx = this.state.program.enrollments.findIndex(year => {
      startTermIdx = year.term_plans.findIndex(term => {
        sourceIdx = term.course_ids.findIndex(id => id === draggableId)
        return sourceIdx !== -1
      })
      return startTermIdx !== -1
    })

    let startYear = this.state.program.enrollments[startYearIdx]
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
      delete newCourses[draggableId]

      let newState = {
        ...this.state,
      }

      // make modifications to state
      newState.courses = newCourses
      newState.program.enrollments[startYearIdx] = newYear

      // set state, then update program in the new state
      this.setState(newState)
      this.updateProgram(newState)
  }

  // this one gets one course at a time
  async getCourseInfo(draggableId: string): Promise<void> {
    // fetches information about this course's offerings
    // and modifies the state's courses
    var request = new Request(API_ADDRESS + `/${draggableId}/course_info.json`, {
      method: 'GET',
      headers: new Headers()
    })

    // need to do this before isCourseOffered() is checked
    let response = await fetch(request);
    let course = await response.json();
    
    let newState = {
      ...this.state,
    }
    newState.courses[draggableId] = course

    await this.setState(newState)

  }



  newCourse(draggableId: string, destYearIdx: number, destTermIdx: number, destIdx: number) {
    // when you drag something from "add" box to somewhere on a term
    let newState = {
      ...this.state,
    }

    // push this course onto the right term plan (in the right idx)
    newState.program.enrollments[destYearIdx].term_plans[destTermIdx].course_ids.splice(destIdx, 0, draggableId)
    newState.add_course = undefined
    this.setState(newState)
    this.updateProgram(newState)
  }

  onDragEnd = (result: DropResult) => {

    const { destination, source, draggableId } = result
    console.log(destination)
    console.log(source)
    console.log(draggableId)

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
    let [destTermId, destYearId] = destination.droppableId.split(" ").map(s => parseInt(s))

    let destYearIdx = this.state.program.enrollments.findIndex(year => year.year === destYearId)
    let destYear = this.state.program.enrollments[destYearIdx]

    let destTermIdx = destYear.term_plans.findIndex(term => term.term === destTermId)
    let destTerm = destYear.term_plans[destTermIdx]

    // see if you are adding a course to the TimeLineContext
    if (source.droppableId === "Add") {
      this.newCourse(draggableId, destYearIdx, destTermIdx, destination.index)
      return
    }

    if(!this.isCourseOffered(draggableId, destTerm, destYear)) {
      this.resetTermHighlights()
      return
    }

    let startYearIdx = destYearIdx
    let startYear = destYear
    if(startYearId !== destYearId) {
      startYearIdx = this.state.program.enrollments.findIndex(year => year.year === startYearId)
      startYear = this.state.program.enrollments[startYearIdx]
    }

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

  isCourseOffered(courseId: string, term: TermState, year: YearState) {
    const termsOffered = this.state.courses[courseId].terms
    const isOffered = termsOffered.findIndex(offering => 
      offering.term === term.term && offering.year === year.year
    )
    return isOffered !== -1
  }

  onDragStart = async (start: DragStart) => {
    const { draggableId, source } = start

    // get offering info for this new course
    if (source.droppableId === "Add") {
      await this.getCourseInfo(draggableId);
    }

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

  updateDuration(updateVal : number) {
    let newState = {
      ...this.state
    }
    newState.program.duration += updateVal
    this.setState(newState)

    console.log(this.state)
  }

  
  render() {
    if(!this.state) return <div></div>

    const program = this.state.program
    this.addMissingTerms()
    return (
      <div>
        <Navbar bg="dark" variant="dark" id="navbar">
          <Navbar.Brand href="/">OnCourse</Navbar.Brand>
          <Nav className="mr-auto">
          </Nav>
          <NavButton id="save" variant="outline-info" onClick={this.savePlan}><i className="fa fa-save"></i></NavButton>
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
                <LColumn> 
                  <div id="timeline">
                    {
                      program.enrollments.map(year => (
                          <div>
                              <Container key={year.year}>
                                {year.term_plans.map(term => {
                                  const courses = term.course_ids.map(course_id => this.state.courses[course_id]!);
                                  const term_tag = term.term.toString() + " " + year.year.toString()
                                  return <Term 
                                            key={term_tag} 
                                            termId={term_tag} 
                                            courses={courses} 
                                            highlight={term.highlight} 
                                            removeCourse={this.removeCourse.bind(this)}/>;
                                })}
                              </Container>
                          </div>
                        )
                      )
                    } 
                  </div>
                  <YearButton onClick={() => this.updateDuration(1)}>++</YearButton>
                  <YearButton onClick={() => this.updateDuration(-1)}>--</YearButton>
                </LColumn> 
                <RColumn>
                  <InfoBar 
                    degree_id={this.state.program.id}
                    degree_name={this.state.program.name}
                    degree_reqs={this.state.program.reqs}
                    add_course={this.state.add_course}
                    add_event={this.addCourse.bind(this)}
                    remove_course={this.removeCourse.bind(this)}

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
