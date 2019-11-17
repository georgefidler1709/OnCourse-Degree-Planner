import React from 'react';
import styled from 'styled-components';
import CourseDropBox from "./CourseDropBox"
import { SearchCourses } from "../degree_search/Search"
import { Course } from "../../Api"
import { Accordion, Card, Button } from 'react-bootstrap'
const Container = styled.div`
  padding: 8px 0px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 350px;
  height: 1000px;
  text-align: center;
  overflow-y: scroll;
  font-family: Arial, Helvetica, sans-serif;
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
  font-family: inhert;
  color: inherit;
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
  
`

interface Req {
  filter_type: string;
  units: number;
  info: string;
}

interface InfoBarProps {
  degree_id: number;
  degree_name: string;
  degree_reqs: Array<Req>;
  add_course?: Course; // Course to add
  add_event: (course: Course) => void;// function to call when you want to add a course
  remove_course: (id: string) => void;
}

function InfoBar(props: InfoBarProps) {
  return (
    <Container>
        <Title>
          {props.degree_name}
          <br/>
          {props.degree_id.toString()}
        </Title>

    <Accordion defaultActiveKey="2">
    <Section bg="dark" text="white">
      <Accordion.Toggle as={SectionHeader} eventKey="1">
      <SubTitle>Add a Course</SubTitle>
      </Accordion.Toggle>
    <Accordion.Collapse eventKey="1">
      <Card.Body>
        <p>Search for a course and click on it. Then drag the course into your timeline from the <b>Add</b> box.</p>
        <CourseDropBox type="Add" add_course={props.add_course} remove_course={props.remove_course}/>
        <SearchCourses add_event={props.add_event}/></Card.Body>
    </Accordion.Collapse>
    </Section>
  </Accordion>
  <Accordion defaultActiveKey="2">
  <Section bg="dark" text="white">
      <Accordion.Toggle as={SectionHeader} variant="link" eventKey="0">
      <SubTitle>Requirements</SubTitle>
      </Accordion.Toggle>
    <Accordion.Collapse eventKey="0">
      <Card.Body>
        <ReqContainer>
          {props.degree_reqs.map(req => { return (
            <div key={req.info}>
              <p>{`${req.filter_type}: ${req.units} UOC of`}</p>
              <ul>
                <li>{`${req.info}`}</li>
              </ul>
            </div>
          )
          })}
        </ReqContainer></Card.Body>
    </Accordion.Collapse>
  </Section>

</Accordion>
        
    </Container>
  );
}

export default InfoBar
