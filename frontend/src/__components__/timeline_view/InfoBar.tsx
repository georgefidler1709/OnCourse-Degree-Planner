import React, {useState} from 'react';
import styled from 'styled-components';
import CourseDropBox from "./CourseDropBox"
import { SearchCourses } from "../degree_search/Search"
import { RemainReq, Course } from "../../Api"
import { Req } from "../../Types"
import Requirements from "./Requirements"
import { Card, Collapse } from 'react-bootstrap'

const Container = styled.div`
  padding-top: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 350px;
  height: 100%;
  text-align: center;
  overflow-y: scroll;
  overflow: overlay;
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

const SubTitle = styled.h5`
  padding: 4px;
  text-align: center;
  width: 100%;
`;

const ReqContainer = styled.div`
  padding: 4px;
  margin-bottom: 4px;
  font-family: inherit;
  text-align: left;
  color: inherit;
`;

const Section = styled(Card)`
`

const SectionHeader = styled(Card.Header)`
  transition: color 0.2s ease;
  color: rgba(255, 255, 255, 0.75);
  display: flex;
  align-items: center

  &:hover {
    color: rgba(255, 255, 255, 1)
  };

`
const SectionIcon = styled.i`
  float: left;
`

interface InfoBarProps {
  degree_id: number;
  degree_name: string;
  degree_reqs: Array<RemainReq>;
  add_course?: Course; // Course to add
  add_event: (course: Course) => void;// function to call when you want to add a course
  remove_course: (id: string) => void;
}

function InfoBar(props: InfoBarProps) {

  const [openAdd, setOpenAdd] = useState(true);
  const [openReqs, setOpenReqs] = useState(false);

  return (
    <Container>
        <Title>
          {props.degree_name}
          <br/>
          {props.degree_id.toString()}
        </Title>
        <Section bg="dark" text="white">
        <SectionHeader
        onClick={() => setOpenAdd(!openAdd)}
        aria-controls="collapse-add-course"
        aria-expanded={openAdd}
      >
        <SectionIcon className={openAdd ? "fa fa-chevron-down" : "fa fa-chevron-left"}/>
        <SubTitle>Add a Course</SubTitle>
      </SectionHeader>
      <Collapse in={openAdd}>
      <Card.Body>
        <p>Search for a course and click on it. Then drag the course into your timeline from the <b>Add</b> box.</p>
        <CourseDropBox type="Add" add_course={props.add_course} remove_course={props.remove_course}/>
        <SearchCourses add_event={props.add_event}/></Card.Body>
      </Collapse>
      </Section>

      <Section bg="dark" text="white">
        <SectionHeader
        onClick={() => setOpenReqs(!openReqs)}
        aria-controls="collapse-requirements"
        aria-expanded={openReqs}
      >
        <SectionIcon className={openReqs ? "fa fa-chevron-down" : "fa fa-chevron-left"}/>
        <SubTitle>Requirements</SubTitle>
      </SectionHeader>
      <Collapse in={openReqs}>
      <Card.Body>
        <ReqContainer>
          <Requirements degree_reqs={props.degree_reqs}/>
        </ReqContainer></Card.Body>
      </Collapse>
      </Section>
    </Container>
  );
}

export default InfoBar
