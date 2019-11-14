import React, { Component, ChangeEvent } from 'react'
import {Suggestions, CourseSuggestions} from './Suggestions'
import {API_ADDRESS} from '../../Constants'
import {SimpleDegrees, SimpleDegree, CourseList, Course} from '../../Api'
import {SearchResult, CourseSearchResult} from '../../Types'
import styled from 'styled-components';

const Container = styled.div`
  padding: 20px;
  margin: 0;
  text-align: center;
`

const SearchBar = styled.input`
  width: 50%;
  padding: 12px 24px;
  margin-bottom: 10px;

  transition: background-colour .2s ease-in;
  font-size: 14px;
  line-height: 18px;

  color: #575756;
  background-color: transparent;
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/%3E%3Cpath d='M0 0h24v24H0z' fill='none'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-size: 18px 18px;
  background-position: 95% center;
  border-radius: 50px;
  border: 1px solid #575756;

  &:hover {
    outline: none;
  }

  &:hover {
    background-color: #f1;
  }
`

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

interface SearchCourseProps {
  add_event: (course: Course) => void;
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

    console.log(this.state.degrees);
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
      <Container>
        <form>
          <SearchBar
            placeholder="Search for your degree..."
            //value={this.state.query}
            onChange={this.handleInputChange}
          />
        </form>
      {
        this.state.searchResults.length > 0 &&
        <Suggestions degrees={this.state.searchResults} />
        }
      </Container>
      )
  }
}

export default Search

class SearchCourses extends Component<SearchCourseProps, SearchCourseState> {
  constructor(props: SearchCourseProps) {
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
      <Container>
        <form>
          <SearchBar
            placeholder="Search for a course..."
            //value={this.state.query}
            onChange={this.handleInputChange}
          />
        </form>
      {
        this.state.searchResults.length > 0 &&
        <CourseSuggestions courses={this.state.searchResults} add_event={this.props.add_event}/>
        }
      </Container>
      )
  }
}

export { SearchCourses };
