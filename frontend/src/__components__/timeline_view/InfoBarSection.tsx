/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * InfoBarSection.tsx
 * Component that represents a single dropdown section in the info bar
 */

import React, { FunctionComponent } from 'react';
import styled from 'styled-components';

import { Card, Collapse } from 'react-bootstrap'

const SubTitle = styled.h5`
  padding: 4px;
  text-align: center;
  width: 100%;
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

interface InfoBarSectionProps {
  open: boolean,
  setOpen: (open: boolean) => void,
  title: string,
}

const InfoBarSection: FunctionComponent<InfoBarSectionProps> = (props) => {
  return (
    <Section bg="dark" text="white">
        <SectionHeader
        onClick={() => props.setOpen(!props.open)}
        aria-controls="collapse-add-course"
        aria-expanded={props.open}
        >
        <SectionIcon className={props.open ? "fa fa-chevron-down" : "fa fa-chevron-right"}/>
        <SubTitle>{props.title}</SubTitle>
    </SectionHeader>
    <Collapse in={props.open}>
      {props.children}
    </Collapse>
    </Section>
  );
}

export default InfoBarSection
