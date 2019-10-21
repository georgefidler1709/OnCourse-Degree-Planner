import React, { Component } from 'react'
import Suggestions from './Suggestions'


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
    // fetch("")
    // .then(response => response.json())
    // .then(response => {
    //    const {suggestedDegrees} = response.data
        const suggestedDegrees = [{id: 1, name:"COMP3778", description: "Bachelor of Computer Science (2019)"}, {id: 2, name:"COMP3978", description: "Bachelor of Computer Science (2016)"}]
        this.setState({
            degrees: suggestedDegrees
        })
        
    //})
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
