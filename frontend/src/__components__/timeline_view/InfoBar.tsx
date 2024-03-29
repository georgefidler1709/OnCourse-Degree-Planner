/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * InfoBar.tsx
 * Controls the sidebar on the right hand side of the timeline view
 * Displays information such as degree requirements as well as adds new courses into the timeline
 */

import React, {useState} from 'react';
import styled from 'styled-components';
import InfoBarDropBox from "./InfoBarDropBox"
import InfoBarSection from "./InfoBarSection"
import { SearchCourses } from "../degree_search/Search"
import { RemainReq, Course } from "../../Api"
import { Requirements, Notes } from "./Requirements"
import { Card } from 'react-bootstrap'

const Container = styled.div`
  &::-webkit-scrollbar {
    display: none;
  }

  padding-top: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 350px;
  max-height: 90vh;
  overflow-y: auto;
  box-sizing: content-box;
  text-align: center;
  background-color: #343a40;
  color: white;
`;

const Title = styled.h3`
  padding: 8px;
  margin: 0px;
  font-family: inherit;
  border-bottom: 1px solid lightgrey;
  color: inherit;
`;

const ReqContainer = styled.div`
  padding: 4px;
  margin-bottom: 4px;
  font-family: inherit;
  text-align: left;
  color: inherit;
`;

interface InfoBarProps {
  degree_id: string;
  degree_name: string;
  degree_reqs: Array<RemainReq>;
  full_reqs: Array<RemainReq>;
  degree_notes: Array<string>;
  standby_courses: Array<Course>;
  done_courses: Array<Course>;
  year: number;
  add_event: (code: string) => Promise<boolean>; // function to call when you want to add a course
  remove_course: (id: string) => void;
  already_enrolled: (code: string) => boolean;
}

function InfoBar(props: InfoBarProps) {

  const [openAdd, setOpenAdd] = useState(true);
  const [openDone, setOpenDone] = useState(false);
  const [openReqs, setOpenReqs] = useState(false);
  const [openFullReqs, setOpenFullReqs] = useState(false);

  return (
    <Container>
      <Title>
        {props.degree_name}
        <br/>
        {props.degree_id.toString()}
      </Title>

      <InfoBarSection 
        open={openAdd} 
        setOpen={setOpenAdd}
        title={"Add a Course"}
      >
          <Card.Body>
            <p>Search for a course and click on it. Then drag the course into your timeline from the <b>Tray</b>.</p>
            <InfoBarDropBox 
              name="Tray" 
              id="Add" 
              courses={props.standby_courses} 
              highlight={false}
              termWarning={false}
              removeCourse={props.remove_course}/>
            <SearchCourses add_event={props.add_event} already_enrolled={props.already_enrolled}/>
          </Card.Body>
      </InfoBarSection>

      <InfoBarSection 
        open={openDone} 
        setOpen={setOpenDone}
        title={"Courses Already Done"}
      >
          <Card.Body>
            <p>Drop the courses you have already done into the box below</p>
            <InfoBarDropBox 
              name="Already Done" 
              id="Done" 
              courses={props.done_courses} 
              highlight={false}
              termWarning={false}
              removeCourse={props.remove_course}/>
          </Card.Body>
      </InfoBarSection>

      <InfoBarSection 
        open={openReqs} 
        setOpen={setOpenReqs}
        title={"Remaining Requirements"}
      >
        <Card.Body>
          <ReqContainer>
            <Requirements degree_reqs={props.degree_reqs} say_remain={true}/>
          </ReqContainer>
        </Card.Body>
      </InfoBarSection>

      <InfoBarSection 
        open={openFullReqs} 
        setOpen={setOpenFullReqs}
        title={"Full Degree Requirements"}
      >
        <Card.Body>
          <ReqContainer>
            <Requirements degree_reqs={props.full_reqs} say_remain={false}/>
            <Notes notes={props.degree_notes}/>
          </ReqContainer>
        </Card.Body>
      </InfoBarSection>
    </Container>
  );
}

export default InfoBar
