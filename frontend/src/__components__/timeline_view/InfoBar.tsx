import React from 'react';
import styled from 'styled-components';
import CourseDropBox from "./CourseDropBox"
import { SearchCourses } from "../degree_search/Search"
import { Course } from "../../Api"

const Container = styled.div`
  margin: 8px;
  padding: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 400px;
  display: flex;
  flex-direction: column;
  text-align: center;
  position: fixed;
`;

const Title = styled.h3`
  padding: 8px;
`;

const SubTitle = styled.h5`
  padding: 4px;
`;

interface Req {
  filter_type: string;
  units: number;
  info: string;
}

interface InfoBarProps {
  degree_id: number;
  degree_name: string;
  degree_reqs: Array<Req>;
  add_course: Course; // Course to add
  add_event: (course: Course) => void;// function to call when you want to add a course
  remove_course: (id: string) => void;
}

function InfoBar(props: InfoBarProps) {
  return (
    <Container>
      <header>
        <Title>{props.degree_name}</Title>
        <Title>{props.degree_id.toString()}</Title>
      </header>
      <body>
        <SubTitle>Requirements</SubTitle>
        {props.degree_reqs.map(req => { return (
          <div>
            <p>{`${req.filter_type}: ${req.units} UOC of`}</p>
            <ul>
              <li>{`${req.info}`}</li>
            </ul>
          </div>
        )
        })}
      </body>
      <footer>
        <CourseDropBox type="Add" add_course={props.add_course} remove_course={props.remove_course}/>
        <SearchCourses add_event={props.add_event}/>
      </footer>
    </Container>
  );
}

export default InfoBar
