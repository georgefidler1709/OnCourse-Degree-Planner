import React from 'react';
import styled from 'styled-components';
import CourseDropBox from "./CourseDropBox"
import { SearchCourses } from "../degree_search/Search"
import { RemainReq, Course } from "../../Api"
import { SubTitle } from '../../Types';

const Container = styled.div`
  margin: 8px;
  padding: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 350px;
  height: 1000px;
  text-align: center;
  overflow-y: scroll;
`;

const Title = styled.h3`
  padding: 8px;
  font-family: Arial, Helvetica, sans-serif;
  border-bottom: 1px solid lightgrey;
`;

const ReqContainer = styled.div`
  padding: 4px;
  margin-bottom: 4px;
  font-family: Arial, Helvetica, sans-serif;
  border-bottom: 1px solid lightgrey;

`;

interface InfoBarProps {
  degree_id: number;
  degree_name: string;
  degree_reqs: Array<RemainReq>;
  add_course?: Course; // Course to add
  add_event: (course: Course) => void;// function to call when you want to add a course
  remove_course: (id: string) => void;
}

function InfoBar(props: InfoBarProps) {
  return (
    <Container>
      <header>
        <Title>{props.degree_name}<br/><br/>{props.degree_id.toString()}</Title>
      </header>
      <body>
        <SubTitle>Requirements</SubTitle>
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
        </ReqContainer>
        <SubTitle>Add a Course</SubTitle>
        <p>Search for a course and click on it. Then drag the course into your timeline from the <b>Add</b> box.</p>
        <CourseDropBox type="Add" add_course={props.add_course} remove_course={props.remove_course}/>
        <SearchCourses add_event={props.add_event}/>
      </body>
      <footer>
      </footer>
    </Container>
  );
}

export default InfoBar
