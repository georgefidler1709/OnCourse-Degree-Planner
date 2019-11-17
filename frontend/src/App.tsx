
import Search from "./__components__/degree_search/Search"
import Timeline from "./__components__/timeline_view/Timeline";
import React from "react";
import styled from 'styled-components';
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

const FullScreenDiv = styled.div`
  height: 100%;
  margin: 0;
`

export default function App() {
  return (
    <div>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"></link>
      <Router>
        <FullScreenDiv>
          <Switch>
            <Route path="/:degree" render={(props) => <Timeline {...props} />}/>
            <Route path="/" render={(props) => <Search {...props} />}/>>
          </Switch>
        </FullScreenDiv>
      </Router>
    </div>
  );
}