import React, {useState, RefObject} from 'react';
import styled from 'styled-components';
import CourseDropBox from "./CourseDropBox"
import InfoBarSection from "./InfoBarSection"
import { SearchCourses } from "../degree_search/Search"
import { RemainReq, Course } from "../../Api"
import { CourseSearchResult } from "../../Types"
import Requirements from "./Requirements"
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
  degree_id: number;
  degree_name: string;
  degree_reqs: Array<RemainReq>;
  add_course?: Course; // Course to add
  add_event: (course: Course, searchRef: RefObject<HTMLInputElement>, searchResults: Array<CourseSearchResult>) => void;// function to call when you want to add a course
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

      <InfoBarSection 
        open={openAdd} 
        setOpen={setOpenAdd}
        title={"Add a Course"}
      >
          <Card.Body>
            <p>Search for a course and click on it. Then drag the course into your timeline from the <b>Add</b> box.</p>
            <CourseDropBox type="Add" add_course={props.add_course} remove_course={props.remove_course}/>
            <SearchCourses add_event={props.add_event}/>
          </Card.Body>
      </InfoBarSection>

      <InfoBarSection 
        open={openReqs} 
        setOpen={setOpenReqs}
        title={"Requirements"}
      >
        <Card.Body>
          <ReqContainer>
            <Requirements degree_reqs={props.degree_reqs}/>
          </ReqContainer>
        </Card.Body>
      </InfoBarSection>
    </Container>
  );
}

export default InfoBar
