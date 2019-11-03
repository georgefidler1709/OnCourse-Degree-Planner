import React, { Component, ChangeEvent } from 'react'
import Suggestions from './Suggestions'
import {API_ADDRESS} from './Constants'
import {SimpleDegrees} from './Api'

class Search extends Component<{}, {query: string; degrees: SimpleDegrees}> {
  constructor(props: {}) {
    super(props)
    this.state = {
      query: '',
      degrees: [],
    }
    this.handleInputChange = this.handleInputChange.bind(this)
  }

  getDegrees(): void {
    fetch(API_ADDRESS + '/degrees.json')
    .then(response => response.json())
    .then(degrees => {
      this.setState({ degrees })
    })
  }

  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
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
