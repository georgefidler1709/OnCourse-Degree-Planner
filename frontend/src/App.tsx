
import Search from "./__components__/degree_search/Search"
import Timeline from "./__components__/timeline_view/Timeline";
import React from "react";
import {
  BrowserRouter as Router,
  Switch,
  Route
} from "react-router-dom";

export default function App() {
  return (
    <Router>
      <div>
        <Switch>
          <Route path="/:degree" render={(props) => <Timeline {...props} />}/>
          <Route path="/" render={(props) => <Search {...props} />}/>>
        </Switch>
      </div>
    </Router>
  );
}