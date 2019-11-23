/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * InfoBarDropBox.tsx
 * Component for dropbox that exist on the infobar
 */

import CourseDropBox from './CourseDropBox';
import styled from 'styled-components';

const Container = styled.div`
  margin: 8px;
  border: 1px solid lightgrey;
  border-radius: 2px;
  width: 220px;

  margin-left: auto;
  margin-right: auto;

  display: flex;
  flex-direction: column;
`;
const Title = styled.h5`
  padding: 8px;
`;
//const CourseList = styled.div`
//  padding: 8px;
//  flex-grow: 1;
//  min-height: 50px;
//`;

const InfoBarDropBox = CourseDropBox(Container, Title);
export default InfoBarDropBox
