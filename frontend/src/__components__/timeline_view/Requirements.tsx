import React from 'react';
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

function Requirements(props: ReqProps) {
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
    return(
      <React.Fragment key={k}>
        <p>{`${k}: ${combo_reqs[k].units} UOC of`}</p>
        <ul>
          {
            combo_reqs[k].items.map(it => {
              return <li>{`${it}`}</li>;
            })
          }
        </ul>
      </React.Fragment>
    )
  })

  return <div>{res}</div>;
}

export default Requirements