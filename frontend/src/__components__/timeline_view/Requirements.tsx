import React from 'react';
import styled from 'styled-components';
import { Req } from "../../Types"

interface ReqProps {
  degree_reqs: Array<Req>;
}

interface PrettyReq {
  units: number;
  items: Array<string>;
}

// Filter types in reqs.filter_type
// - 'OrFilter'
// - 'AndFilter'
// - 'FreeElective'
// - 'GenEd'
// - 'Level'
// - 'SpecificCourse'

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

function allRequirementsMet(degree_reqs: Array<Req>) {
  return degree_reqs.length === 0
}

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
    // <span style={{color: '#3F94B6'}}>
    var res = keys.map(k => {
      return(
        <React.Fragment key={k}>
          <CounterContainer>
          <ReqTitle>{`${k}`}</ReqTitle>
          <p><span style={{color: '#17a2b8'}}><u>{`${combo_reqs[k].units} UOC`}</u>{' remaining'}</span></p>
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
    })

    return <div>{res}</div>;
  }
 
 
}

export default Requirements;
export { Requirements };

interface NoteProps {
  notes: Array<string>;
}


// simple notes about the degree to display in a list
// make the text small as it's verbose
function Notes(props: NoteProps) {
  if (props.notes.length > 0) {
    var res = props.notes.map(note => (<li>{`${note}`}</li>))

    return (<div><ReqTitle>Other requirements to note</ReqTitle><ul>{res}</ul></div>);
  } else {
    return <div></div>;
  }
  
}

export { Notes };
