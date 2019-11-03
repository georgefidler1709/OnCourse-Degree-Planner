
import Search from "./Search"
import Timeline from "./Timeline";
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
          <Route path="/timeline" render={(props) => <Timeline {...props} />}/>
          <Route path="/" render={(props) => <Search {...props} />}/>>
        </Switch>
      </div>
    </Router>
  );
}