import React from 'react';
import { Req } from "../../Types"

interface ReqProps {
  degree_reqs: Array<Req>;
}

function Requirements(props: ReqProps) {
  var res = props.degree_reqs.map(req => {
      return (
        <React.Fragment key={req.info}>
          <p>{`${req.filter_type}: ${req.units} UOC of`}</p>
          <ul>
            <li>{`${req.info}`}</li>
          </ul>
        </React.Fragment>
      )
    }
  )

  return <div>{res}</div>;
}

export default Requirements