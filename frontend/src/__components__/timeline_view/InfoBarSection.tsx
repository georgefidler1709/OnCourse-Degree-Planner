import React from 'react';
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
  children: JSX.Element[] | JSX.Element
}

function InfoBarSection (props: InfoBarSectionProps) {
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
