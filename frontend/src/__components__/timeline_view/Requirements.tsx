import React from 'react';
import { RemainReq, CourseReq } from "../../Api"
import { SubTitle } from "../../Types"

interface RequirementsProps {
  title: string;
  degree_reqs: Array<CourseReq>;
}

function instanceOfRemainReq(a: CourseReq): a is RemainReq {
  return 'units' in a;
}


function Requirements(props: RequirementsProps) {
  function getUnitsIfExist(a: CourseReq): string {
    if(instanceOfRemainReq(a)) {
      return `${a.units} UOC of`;
    }
    else {
      return '';
    }
  }

  return (<>
  <SubTitle>{props.title}</SubTitle>
    {props.degree_reqs.map(req => { return (
      <div key={req.info}>
        <p>{`${req.filter_type}: ` + getUnitsIfExist(req)}</p>
      <ul>
        <li>{`${req.info}`}</li>
      </ul>
    </div>
    )
    })}
    </>);
}

export default Requirements;
