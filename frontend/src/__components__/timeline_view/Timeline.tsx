/**
* COMP4290 Group Project
* Team: On Course
* Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
* George Fidler (z5160384), Kevin Ni (z5025098)
* 
* Timeline.tsx
* Main component for the timeline view of a degree plan.
*/



import React, {Component} from 'react';
import '@atlaskit/css-reset';
import styled from 'styled-components';
import { Navbar, Nav, Button } from 'react-bootstrap'
import { DragDropContext, DropResult, DragStart } from 'react-beautiful-dnd';
import html2canvas from 'html2canvas'
import { saveAs } from 'file-saver'
import { RouteComponentProps } from 'react-router-dom';
import { CheckResponse } from '../../Api';
import {API_ADDRESS, DB_YEAR_MAX } from '../../Constants'
import { TimelineState, YearState } from '../../Types'
import Term from './Term';
import InfoBar from "./InfoBar"


const TimeLineContext = styled.div`
  display: flex;
  justify-content: center;
  margin: 0px;
  padding: 0px;
`;
const Container = styled.div`
  display: flex;
  margin: 0px;
  padding: 0px;
`;

const LColumn = styled.div`
  float: left;
  width: 70%;
  padding: 10px;
`;

const RColumn = styled.div`
  display: flex;
  justify-content: flex-end;
  margin: 0px;
  padding: 0px;
  width: 30%;
  overflow: hidden;
  position: -webkit-sticky;
  position: sticky;
  top: 0;
`;

const Logo = styled.img`
  width: 5%;
  height: 5%;
  margin: 1%;
`

const NavButton = styled(Button)`
  margin: 0px 8px;
`;

const YearButton = styled(Button)`
&& {
  display: inline-block;
  font-weight: 400;
  font-size: 30px;
  padding: .375rem .75rem;
  border: 1px solid transparent;
  border-radius: .25rem;
  transition: color .15s ease-in-out,background-color .15s ease-in-out,border-color .15s ease-in-out,box-shadow .15s ease-in-out;
}
  min-width: 55px;
  margin: 6px;
  text-align: center;
  vertical-align: middle;
  padding: 0px;
`

 /**
 * Main component for the timeline view for a degree plan
 */
class Timeline extends Component<RouteComponentProps<{degree: string}>, TimelineState> {

  constructor(props: RouteComponentProps<{degree: string}>) {
    super(props)
    let code = props.location.pathname;
    fetch(API_ADDRESS + `${code}/gen_program.json`)
    .then(response => response.json())
    .then(plan => {
      this.setState({
        ...plan, 
        add_course: [],
		accepted_overload: false,
      }) 
      this.addMissingTerms()
    }).catch(error => console.error(error));
  }

 /**
 * Fills out a degree plan with empty terms to be represented on the timeline view
 * so that there will be a container representing every term for 
 * the duration of the degree.
 */
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
  }

 /**
 * Check if the current plan contains a given course
 */
  isEnrolled(course: string): boolean {
    return course in this.state.courses;
  }

 /**
 * Check if the current plan has any enrollments in a given year
 */
  isYearEmpty(year: YearState) {
    return year.term_plans.findIndex(term => term.course_ids.length > 0) === -1;
  }

/**
 * Attempt to remove a year from the timeline.
 * Succeeds if the year does not have any courses assigned to it.
 * If it fails the user is alerted
 */
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

  /**
  * function to pass to CourseSuggestions in Suggestions.tsx via InfoBar's SearchCourse
  * sets this.state.add_course to be the Course passed in
  */
  async addCourse(code: string) {
    // if already have this course on timeline, then can't enroll in it
    if (this.isEnrolled(code)) {
      alert(`You already have ${code} on your timeline.`)
      return false;
    } else {
      // fetches information about this course's offerings
      // and modifies the state's courses
      let response = await fetch(API_ADDRESS + `/${code}/course_info.json`);
      let course = await response.json();

      this.setState(state => {
        state.add_course.push(course.code)
        return {
          add_course: state.add_course,
          courses: {
            ...state.courses,
            [course.code]: course
          }
        };
      })
      return true;
    }
  }

  /**
  * Adds an new empty term to the timeline view
  */
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

  /**
  * Adds an new empty year to the timeline view
  */
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

  /**
  * Takes the current program in state,
  * assuming it has been modified,
  * and updates it via an API call to /check_program.json
  */
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
    .then((reqs: CheckResponse) => {
      this.setState({reqs}); 
      this.addMissingTerms();
    }).catch(error => console.error(error));
  }

  /**
   * Removes a given course from the timeline view
   */
  removeCourse(courseId: string) {
    let sourceIdx = -1
    let startTermIdx = -1
    let startYearIdx = -1

    let newState = {
      ...this.state,
    }

    // find given course
    let findArray = () => {
      if ((sourceIdx = newState.add_course.findIndex(id => id === courseId)) !== -1) {
        return newState.add_course;
      }
      else if ((sourceIdx = newState.program.done.findIndex(id => id === courseId)) !== -1) {
        return newState.program.done;
      }
      else {
        startYearIdx = newState.program.enrollments.findIndex(year => {
          startTermIdx = year.term_plans.findIndex(term => {
            sourceIdx = term.course_ids.findIndex(id => id === courseId)
            return sourceIdx !== -1
          })
          return startTermIdx !== -1
        })

        // remove it
        return newState.program.enrollments[startYearIdx].term_plans[startTermIdx].course_ids;
      }
    }

    findArray().splice(sourceIdx, 1)
    delete newState.courses[courseId];
    // set state, then update program in the new state
    this.setState(newState)
    this.updateProgram(newState)
  }

  /**
   * Add a new course to the timeline view from the add tray
   */
  newCourse(draggableId: string, destYearIdx: number, destTermIdx: number, destIdx: number, sourceIdx: number) {
    // when you drag something from add tray to somewhere on a term
    let newState = {
      ...this.state,
    }

    // push this course onto the right term plan (in the right idx)
    newState.add_course.splice(sourceIdx, 1);
    newState.program.enrollments[destYearIdx].term_plans[destTermIdx].course_ids.splice(destIdx, 0, draggableId)
    this.setState(newState)
    this.updateProgram(newState)
    this.resetTermHighlights()
  }

  /**
  * Eventhandler called when the user drops a course object after a drag
  * Determines the new location of the course and updates state accordingly
  */
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
    
    let [termId, yearId] = destination.droppableId.split(" ").map(s => parseInt(s));
    if(termId && yearId && !this.isCourseOffered(draggableId, termId, yearId)) {
      this.resetTermHighlights()
      return;
    }
    /**
     * Determines the location in state
     * represented by the location in which the course was dropped
     */
    function getTarget(state: TimelineState, id: string): Array<string> {
      if(id === "Add") return state.add_course;
      if(id === "Done") return state.program.done;
      let [termId, yearId] = id.split(" ").map(s => parseInt(s))

      let yearIdx = state.program.enrollments.findIndex(year => year.year === yearId);
      let year = state.program.enrollments[yearIdx];
      let termIdx = year.term_plans.findIndex(term => term.term === termId);
      let term = year.term_plans[termIdx];
      return term.course_ids;
    }

    let newState = {
      ...this.state,
    }

    let destIds = getTarget(newState, destination.droppableId);

    let uoc = destIds.reduce((acc, course) => {return newState.courses[course].units + acc}, 0)
      + (destination.droppableId === source.droppableId ? 0 : newState.courses[draggableId].units);

    if (!newState.accepted_overload && termId && yearId && 18 < uoc) {
      var accept = window.confirm("You are overloading. Are you sure?");
      if (!accept) {
        this.resetTermHighlights()
        return;
      }
      newState.accepted_overload = true;
    }

    let sourceIds = getTarget(newState, source.droppableId);
    sourceIds.splice(source.index, 1);
    destIds.splice(destination.index, 0, draggableId);


    this.setState(newState, () => {
      this.updateProgram(newState);
      this.resetTermHighlights();
    });
  };

  /**
   * Reset all terms to the term highlights after a drag has concluded
   */
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

  /**
   * Check if a course is offered in a given term (in a given year)
   */
  isCourseOffered(courseId: string, term: number, year: number) {
    const termsOffered = this.state.courses[courseId].terms
    const isOffered = termsOffered.findIndex(offering => 
      offering.term === term && offering.year === year
    )
    return isOffered !== -1
  }

  /**
   * Event handler called when a user clicks on a course
   * and begins to drag it. 
   * Highlights the term containers in which the course being dragged is offered
   */
  onDragStart = async (start: DragStart) => {
    const { draggableId } = start

    let newEnrollments = this.state.program.enrollments.map(year => {
      let newYear = {
        ...year,
      }
      newYear.term_plans = year.term_plans.map(term => {
        let newTerm = {...term}
        newTerm.highlight = this.isCourseOffered(draggableId, term.term, year.year)
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

  /**
   * Save an image of the current plan
   * to be stored locally for the user
   */
  savePlan() {
    html2canvas(document.getElementById('timeline')!).then(function(canvas) {
      canvas.toBlob(function(blob) {
        // Generate file download
        saveAs(blob!, "plan.png");
    });
  });
  }

  /**
   * Update the duration of the degree plan 
   * i.e. adding or removing a year from the timeline view
   * within the bounds of an acceptable degree plan
   */
  updateDuration(updateVal : number) {
    let newState = {
      ...this.state
    }
    newState.program.duration += updateVal
    newState.program.duration = Math.max(1, newState.program.duration)
    if(newState.program.year + newState.program.duration > DB_YEAR_MAX + 1) {
      newState.program.duration = DB_YEAR_MAX + 1 - newState.program.year
      alert("Degree planning information is not accurate beyond 2025")
    }
    
    this.setState(newState)
    this.addMissingTerms()

  }

  /**
   * Render the timeline view
   */
  render() {
    if(!this.state) return <div></div>

    const program = this.state.program
    return (
      <div>
        <Navbar bg="dark" variant="dark" id="navbar">
          <Navbar.Brand href="/"><Logo src={"/images/logo.png"} alt="logo"/> OnCourse</Navbar.Brand>
          <Nav className="mr-auto">
          </Nav>
          <NavButton id="save" variant="outline-info" onClick={this.savePlan}><i className="fa fa-save"></i></NavButton>
        </Navbar>
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
                          <div key={year.year}>
                              <Container key={year.year}>
                                {year.term_plans.map(term => {
                                  const courses = term.course_ids.map(course_id => this.state.courses[course_id]!);
								  const uoc = courses.reduce((acc, course) => course.units + acc, 0);
                                  const term_tag = term.term.toString() + " " + year.year.toString()

                                  return <Term 
                                            key={term_tag} 
                                            name={term_tag} 
                                            courses={courses} 
                                            highlight={term.highlight} 
											termWarning={uoc > 18}
                                            removeCourse={this.removeCourse.bind(this)}
                                            getError={(s) => this.state.reqs.course_reqs[s]}
                                            getWarn={(s) => this.state.reqs.course_warn[s]}/>;
                                })}
                              </Container>
                          </div>
                        )
                      )
                    } 
                  </div>
                  <YearButton variant="info" onClick={() => this.updateDuration(1)}>+</YearButton>
                  <YearButton variant="info" onClick={() => this.updateDuration(-1)}>-</YearButton>
                </LColumn> 
                <RColumn>
                  <InfoBar 
                    degree_id={this.state.program.id}
                    degree_name={this.state.program.name}
                    degree_reqs={this.state.reqs.degree_reqs}
                    year={this.state.program.year}
                    full_reqs={this.state.full_reqs}
                    degree_notes={this.state.program.notes}
                    standby_courses={this.state.add_course.map(course_id => this.state.courses[course_id]!)}
                    done_courses={this.state.program.done.map(course_id => this.state.courses[course_id]!)}
                    add_event={this.addCourse.bind(this)}
                    remove_course={this.removeCourse.bind(this)}
                    already_enrolled={this.isEnrolled.bind(this)}
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
