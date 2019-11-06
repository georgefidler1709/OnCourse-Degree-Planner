import React, { Component, ChangeEvent } from 'react'
import Suggestions from './Suggestions'
import {API_ADDRESS} from '../../Constants'
import {SimpleDegrees, SimpleDegree} from '../../Api'
import {SearchResult} from '../../Types'

interface SearchState {
  searchResults : Array<SearchResult>;
  degrees: SimpleDegrees
  oldQuery: string
}

class Search extends Component<{}, SearchState> {
  constructor(props: {}) {
    super(props)
    this.state = {
      searchResults: [],
      degrees: [],
      oldQuery: '',
    }
    fetch(API_ADDRESS + '/degrees.json')
    .then(response => response.json())
    .then(degrees => {
      this.setState({ degrees })
    })

    this.handleInputChange = this.handleInputChange.bind(this)
  }


  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    let query = event.target.value.toLowerCase();
    let searchResults: Array<SearchResult> = [];
    console.log(event);

    function processDegree(degree: SimpleDegree) {
      let index = degree.name.toLowerCase().indexOf(query);
      if (index !== -1) {
        let begin = degree.name.substring(0, index);
        let mid = degree.name.substring(index, index + query.length);
        let end = degree.name.substring(index + query.length)
        searchResults.push({
          degree,
          text: <>{begin}<u>{mid}</u>{end}</>
        })
      }
      else if (degree.id.includes(query)) {
        searchResults.push({degree, text: <>{degree.name}</>})
      }
    }

    if (query.length !== 0) {
      if (this.state.oldQuery.length !== 0 && (query.startsWith(this.state.oldQuery) || query.endsWith(this.state.oldQuery))) {
        for (let result of this.state.searchResults) {
          processDegree(result.degree);
        }
      }
      else {
        for (let degree of this.state.degrees) {
          processDegree(degree);
        }
      }
    }
    this.setState({ searchResults, oldQuery: query });
  }

  render() {
    return (
      <div className="search-bar-container">
        <form>
          <input
            className="search-bar"
            placeholder="Search for your degree..."
            //value={this.state.query}
            onChange={this.handleInputChange}
          />
        </form>
      {
        this.state.searchResults.length > 0 &&
        <Suggestions degrees={this.state.searchResults} />
        }
      </div>
      )
  }
}

export default Search
