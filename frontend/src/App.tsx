/**
* COMP4290 Group Project
* Team: On Course
* Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
* George Fidler (z5160384), Kevin Ni (z5025098)
* 
* App.tsx
* Main routing component of the application
* used to direct the user to other pages
*/

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