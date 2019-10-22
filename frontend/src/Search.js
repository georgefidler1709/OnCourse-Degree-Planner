import React, { Component } from 'react'
import Suggestions from './Suggestions'

import {API_ADDRESS} from './Constants'

class Search extends Component {
  constructor() {
    super()
    this.state = {
      query: '',
      degrees: []
    }
    this.handleInputChange = this.handleInputChange.bind(this)
  }

  getDegrees() {
     fetch(API_ADDRESS + '/degrees.json')
     .then(response => response.json())
     .then(degrees => {
        this.setState({
            degrees: degrees
        })
    })
  }

  handleInputChange(event) {
    this.setState({
      query: event.target.value
    })
    this.getDegrees()
  }

 render() {
   return (
     <div className="search-bar-container">
      <form>
        <input
          className="search-bar"
          placeholder="Search for your degree..."
          value={this.state.query}
          onChange={this.handleInputChange}
        />
      </form>
      {
       this.state.degrees.length > 0 && 
       this.state.query.length > 0 &&
       <Suggestions degrees={this.state.degrees} />
      }
     </div>
   )
 }
}

export default Search
