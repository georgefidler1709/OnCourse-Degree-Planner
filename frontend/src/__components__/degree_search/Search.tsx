import fetch from 'node-fetch';
import React, { Component, ChangeEvent } from 'react'
import {Suggestions, CourseSuggestions} from './Suggestions'
import {API_ADDRESS} from '../../Constants'
import {SimpleDegrees, SimpleDegree, CourseList, Course} from '../../Api'
import {SearchResult, CourseSearchResult} from '../../Types'

interface SearchState {
  searchResults : Array<SearchResult>;
  degrees: SimpleDegrees
  oldQuery: string
}

interface SearchCourseState {
  searchResults : Array<CourseSearchResult>;
  courses: CourseList
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
      .catch((error) => console.error(error));

    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    let query = event.target.value.toLowerCase();
    let searchResults: Array<SearchResult> = [];

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

class SearchCourses extends Component<{}, SearchCourseState> {
  constructor(props: {}) {
    super(props)
    this.state = {
      searchResults: [],
      courses: [],
      oldQuery: '',
    }

    fetch(API_ADDRESS + '/full_courses.json')
      .then(response => response.json())
      .then(courses => {
        this.setState({ courses })
      })
      .catch((error) => console.error(error));

    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    let query = event.target.value.toLowerCase();
    let searchResults: Array<CourseSearchResult> = [];

    function processCourse(course: Course) {
      // see if query matches part of name or course code
      let index = course.name.toLowerCase().indexOf(query);
      let textRes = <>{course.name}</>
      if (index !== -1) {
        let begin = course.name.substring(0, index);
        let mid = course.name.substring(index, index + query.length);
        let end = course.name.substring(index + query.length);
        textRes = <>{begin}<u>{mid}</u>{end}</>;
      }

      let codeIndex = course.code.toLowerCase().indexOf(query);
      let codeRes = <>{course.code}</>
      if (codeIndex !== -1) {
        let beginC = course.code.substring(0, codeIndex);
        let midC = course.code.substring(codeIndex, codeIndex + query.length);
        let endC = course.code.substring(codeIndex + query.length);
        codeRes = <>{beginC}<u>{midC}</u>{endC}</>;
      }

      if (index !== -1 || codeIndex !== -1) {
        // matches at least one, display result
        searchResults.push({
          course,
          text: textRes,
          code: codeRes
        })
      }

    }

    if (query.length !== 0) {
      if (this.state.oldQuery.length !== 0 && (query.startsWith(this.state.oldQuery) || query.endsWith(this.state.oldQuery))) {
        for (let result of this.state.searchResults) {
          processCourse(result.course);
        }
      }
      else {
        for (let course of this.state.courses) {
          processCourse(course);
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
            placeholder="Search for a course..."
            //value={this.state.query}
            onChange={this.handleInputChange}
          />
        </form>
      {
        this.state.searchResults.length > 0 &&
        <CourseSuggestions courses={this.state.searchResults} />
        }
      </div>
      )
  }
}

export { SearchCourses };
