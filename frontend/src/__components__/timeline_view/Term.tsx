import React from 'react';
import CourseDropBox from './CourseDropBox';
import styled from 'styled-components';
import { Course as ApiCourse, CourseReq } from '../../Api';

const Container = styled.div`
  margin-top: 8px;
  margin-bottom: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 400px;
  text-align: center;
  display: flex;
  flex-direction: column;
`;
const Title = styled.h3`
  padding: 8px;
  font-family: Arial, Helvetica, sans-serif;
  border-bottom: 1px solid lightgrey;
  margin: 0px;
`;

interface TermProps {
  key: string;
  name: string;
  courses: Array<ApiCourse>;
  highlight: boolean;
  removeCourse: (s: string) => void;
  getError: (s: string) => (Array<CourseReq> | undefined);
  getWarn: (s: string) => (Array<string> | undefined);
}

const TermDropBox = CourseDropBox(Container, Title);
function Term(props: TermProps) {
  return (
    <TermDropBox
      {...props}
      id={props.name}
      name={"T" + props.name}/>
  );
}

export default Term
