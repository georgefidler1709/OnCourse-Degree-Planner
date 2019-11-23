/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910), 
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * Requirements.tsx
 * Implements the display of requirements in the infobar.
 * Does both requirements left to be completed that update dynamically,
 * and static "full requirements" of a degree.
 */

import React from 'react';
import styled from 'styled-components';
import { Req } from "../../Types"

interface ReqProps {
  degree_reqs: Array<Req>;
  say_remain: boolean;
}

interface PrettyReq {
  units: number;
  items: Array<string>;
}

const CounterContainer = styled.div`
  display: flex;
  justify-content: space-between;
`

const ReqTitle = styled.p`
  font-weight: bold;
`

const CongratsMessage = styled.h4`
  font-weight: bold;
  color: #3ae05c;
`

/**
 * Checks if all requirements for a degree are met.
 */
function allRequirementsMet(degree_reqs: Array<Req>) {
  if(degree_reqs !== undefined) {
    return degree_reqs.length === 0
  } else return true
  
}

/**
 * Renders requirements in the form of ReqProps.
 * This includes everything but free-form degree notes.
 */
function Requirements(props: ReqProps) {
  if(allRequirementsMet(props.degree_reqs)) {
    return <CongratsMessage>Good to Graduate!</CongratsMessage>
  } 
  else {
     // combine each requirement type into one heading
    var combo_reqs: Record<string, PrettyReq> = {};

    var keys: Array<string> = [];

    props.degree_reqs.forEach(req => {
      if (req.filter_type in combo_reqs) {
        // add to units and items
        combo_reqs[req.filter_type].units += req.units;
        combo_reqs[req.filter_type].items.push(req.info);
      } else {
        // set to units and items
        combo_reqs[req.filter_type] = {
          units: req.units,
          items: [req.info]
        };

        keys.push(req.filter_type);
      }
    })

    // each item in combo_reqs should be displayed as UOC
    // then a list of items. 
    var res = keys.map(k => {
      if (k) {
        return(
          <React.Fragment key={k}>
              <CounterContainer>
              <ReqTitle>{`${k}`}</ReqTitle>
              <p><span style={{color: '#17a2b8'}}><u>{`${combo_reqs[k].units} UOC`}</u>{props.say_remain && ' remaining'}</span></p>
              </CounterContainer>
              <ul>
                {
                  combo_reqs[k].items.map(it => {
                    return <li key={it}>{`${it}`}</li>;
                  })
                }
              </ul>
          </React.Fragment>
        )
      } else {
        // Total UOC
        return(
          <React.Fragment key="Total">
            <CounterContainer>
            <ReqTitle>> Total UOC count</ReqTitle>
            <p><span style={{color: '#00cc99'}}><u>{`${combo_reqs[k].units} UOC`}</u>{props.say_remain && ' remaining'}</span></p>
            </CounterContainer>
          </React.Fragment>
        )
      }
    })

    return <div>{res}</div>;
  }
 
 
}

export default Requirements;
export { Requirements };

interface NoteProps {
  notes: Array<string>;
}

/**
 * Displays simple notes about a degree that don't fit in the
 * standard Requirements format.
 */
function Notes(props: NoteProps) {
  if (props.notes && props.notes.length > 0) {
    var res = props.notes.map(note => (<li>{`${note}`}</li>))

    return (<div><ReqTitle>Other requirements to note</ReqTitle><ul>{res}</ul></div>);
  } else {
    return <div></div>;
  }
  
}

export { Notes };
