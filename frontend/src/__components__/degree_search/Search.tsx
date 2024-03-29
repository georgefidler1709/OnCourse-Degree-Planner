/**
 * COMP4290 Group Project
 * Team: On Course
 * Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910), 
 * George Fidler (z5160384), Kevin Ni (z5025098)
 *
 * Search.tsx
 * Implementation of search for degrees used on the home page,
 * and search for courses used in the sidebar.
 */

import React, { Component, ChangeEvent, RefObject } from 'react'
import {Suggestions, CourseSuggestions} from './Suggestions'
import {API_ADDRESS, CURRENT_YEAR} from '../../Constants'
import {SimpleDegrees, SimpleDegree, CourseList} from '../../Api'
import {SearchResult, CourseSearchResult} from '../../Types'
import styled from 'styled-components';
import {Dropdown, Form} from 'react-bootstrap'

const Logo = styled.img`
  display: block;
  margin-left: 45%;
  margin-right: auto;
  margin-top: 2%;
  width: 10%;
  height: 10%;
`

const Title = styled.h1`
  float: center;
  text-align: center;
  font-weight: 800;
  font-family: 'Open Sans','Helvetica Neue',Helvetica,Arial,sans-serif;
  font-size: 100px;
`

const SearchContainer = styled.div`
  height: 100%;
  width: 100%;
  margin: 0;
  padding: 20px;
`

const SearchHeader = styled.div`
  display: flex;
  justify-content: center;
`

const SearchBarContainer = styled.div`
  box-shadow: 10px 10px grey;
  display: flex;
  margin-left: auto;
  margin-right: auto;
  width: 60%;
  height: 100%
  margin-bottom: 2%;

  border-radius: 50px;
  border: 1px solid #575756;
`

const YearSelectContainer = styled(Dropdown)`
`
const YearSelect = styled(Dropdown.Toggle)`
  font-weight: bold !important;
  background-color: #00e6ae !important;
  height: 100%;
  width: 100%;
  border-radius: 50px 0px 0px 50px !important;
  border: 1px solid #575756 !important;

  &:focus {
    box-shadow:none !important;
    outline:0px !important;
  }
  &:active {
    box-shadow:none !important;
    outline:0px !important;
  }  
}
`
const YearItem = styled(Dropdown.Item)`
  background-color: ${
  props => props.active ?
      "#00e6ae": "white"
  } !important; 

  &:hover {
    background-color: ${
      props => props.active ?
      "#38ab8f": "#e3e3e3"
      } !important; 
  } 
`

const SearchBar = styled.input`

  &:focus {
    outline: none;
    &::placeholder {
      color: transparent;
    }
  }
  width: 100%;
  height: 100%;
  padding: 1% 4%;
  border-radius: 50px;
  border: none;
  transition: background-colour .2s ease-in;
  font-size: 30px;
  line-height: 18px;
  background-color: transparent;
  background-image: url("data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24'%3E%3Cpath d='M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/%3E%3Cpath d='M0 0h24v24H0z' fill='none'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-size: 40px 40px;
  background-position: 95% center;
`

const SearchForm = styled.form`
  width: 100%;
  height: 11%;
  display: flex;
  flex-direction: column;
`

const Disclaimer = styled.p`
  float: right;
  padding: 20px;
  font-size: 12px;
`

interface SearchState {
  searchResults : Array<SearchResult>
  degrees: SimpleDegrees
  oldQuery: string
  years: Array<number>,
  year: number
}

interface SearchCourseState {
  searchResults : Array<CourseSearchResult>;
  termFilters: Array<boolean>;
  courses: CourseList
}

interface SearchCourseProps {
  add_event: (code: string) => Promise<boolean>;
  already_enrolled: (code: string) => boolean;
}

/**
 * Search for degrees.
 */
class Search extends Component<{}, SearchState> {

  /**
   * Initialises state and fetches the full list of degrees from API.
   */
  constructor(props: {}) {
    super(props)
    this.state = {
      searchResults: [],
      degrees: [],
      oldQuery: '',
      years: [],
      year: CURRENT_YEAR
    }

    fetch(API_ADDRESS + '/degrees.json')
      .then(response => response.json())
      .then(response => {
        this.setState({...response})
      })
      .catch((error) => console.error(error));

    this.handleInputChange = this.handleInputChange.bind(this);
  }

  /**
   * Whenever the user enters a query in search bar,
   * displays a dropdown of search results,
   * and underlines the matching parts of search results.
   */
  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    let query = event.target.value.toLowerCase();
    let searchResults: Array<SearchResult> = [];

    function processDegree(degree: SimpleDegree) {
      // see if query matches part of name or degree id
      let index = degree.name.toLowerCase().indexOf(query);
      let textRes = <>{degree.name}</>
      if (index !== -1) {
        let begin = degree.name.substring(0, index);
        let mid = degree.name.substring(index, index + query.length);
        let end = degree.name.substring(index + query.length)
        textRes = <>{begin}<u>{mid}</u>{end}</>;
      }

      let codeIndex = degree.id.toLowerCase().indexOf(query)
      let codeRes = <>{degree.id}</>
      if (codeIndex !== -1) {
        let beginC = degree.id.substring(0, codeIndex);
        let midC = degree.id.substring(codeIndex, codeIndex + query.length);
        let endC = degree.id.substring(codeIndex + query.length);
        codeRes = <>{beginC}<u>{midC}</u>{endC}</>;
      }

      if (index !== -1 || codeIndex !== -1) {
        // matches at least one, display result
        searchResults.push({
          degree,
          text: textRes,
          code: codeRes
        })
      }
    }

    if(query.length !== 0) {
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

  /**
   * HTML output of search for degrees.
   */
  render() {
    return (
      <SearchContainer>
        <SearchHeader>
          <Logo src={"/images/logo.png"} alt="logo"/>
          <Disclaimer>
            * Disclaimer: OnCourse is not
            <br/> affiliated with or endorsed by UNSW.
            <br/> This product is intended to aid degree planning.
            <br/> However, it should not be the only resourced used
            <br/> in planning your future at university,
            <br/> as it may be subject to error.
          </Disclaimer>
        </SearchHeader>
        <Title>OnCourse</Title>
        <SearchForm>
          <SearchBarContainer>
            <YearSelectContainer>
              <YearSelect variant="light" id="dropdown-basic">
                Start Year: {this.state.year}
              </YearSelect>
              <Dropdown.Menu>
                {
                  this.state.years.map(year => 
                    <YearItem key={year} active={year === this.state.year} onClick={() => this.setState({year: year})}>{year}</YearItem>
                  )
                }
              </Dropdown.Menu>
            </YearSelectContainer>
          <SearchBar
            placeholder="Search for your degree..."
            onChange={this.handleInputChange}
          />
        </SearchBarContainer>
      </SearchForm>
      {
        this.state.searchResults.length > 0 &&
        <Suggestions 
          degrees={this.state.searchResults}
          year={this.state.year}
        />
      }
    </SearchContainer>
    )
  }
}

export default Search

const CoursesContainer = styled.div`
  padding: 3px;
  margin: 0;
  text-align: center;
`

const CourseSearchBar = styled(SearchBar)`

&::placeholder {
  color: rgba(255, 255, 255, 0.75);
}
  width: 95%;
  padding: 12px 24px;
  margin-bottom: 1%;

  font-size: 14px;
  line-height: 18px;
  font-color: white;

  color: white;
  background-size: 18px 18px;
  background-position: 95% center;
  border: 1px solid white;

  box-shadow: 0px 0px;
`

const TermFilterGroup = styled(Form.Group)`
  display: flex;
  justify-content: space-around;
`
const TermFilter = styled(Form.Check)`
`

/**
 * Search functionality for courses in the sidebar once filling out a degree.
 */
class SearchCourses extends Component<SearchCourseProps, SearchCourseState> {
  private searchBarRef: RefObject<HTMLInputElement>

  /**
   * Initialises state and fetches the full list of courses from API.
   */
  constructor(props: SearchCourseProps) {
    super(props)
    this.searchBarRef = React.createRef<HTMLInputElement>()

    this.state = {
      searchResults: [],
      termFilters: [false, false, false],
      courses: [],
    }

    fetch(API_ADDRESS + '/full_courses.json')
      .then(response => response.json())
      .then(courses => {
        this.setState({ courses })
      })
      .catch((error) => console.error(error));

    this.handleInputChange = this.handleInputChange.bind(this);
    this.handleCheckChanged = this.handleCheckChanged.bind(this);
    this.addCourse = this.addCourse.bind(this);
  }

  /**
   * Whenever the user enters a query in search bar,
   * displays a dropdown of search results,
   * and underlines the matching parts of search results.
   */
  handleInputChange(event: ChangeEvent<HTMLInputElement>): void {
    this.search();
  }

  /**
   * performs the search and populates the results
   */
  search(): void {
    let query = this.searchBarRef.current!.value.toLowerCase();
    let searchResults: Array<CourseSearchResult> = [];
    let hasTermFilter = this.state.termFilters.some(x => x);
    let termFilters = this.state.termFilters;

    if (query.length !== 0) {
      for (let course of this.state.courses) {
        // see if query matches part of name or course code
        if (this.props.already_enrolled(course.code)) {
          continue; 
        }

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

        if (hasTermFilter) {
          if(!course.terms.some(x => termFilters[x.term - 1])) {
            continue;
          }
        }

        if (index !== -1 || codeIndex !== -1) {
          // matches at least one, display result
          searchResults.push({
            course,
            text: textRes,
            code: codeRes
          })
          if(searchResults.length >= 50) break;
        }
      }
    }
    this.setState({ searchResults});
  }

  /**
   * Adds a course asynchronously to try and improve performance of loading courses.
   */
  async addCourse(code: string) {
    let success: boolean = await this.props.add_event(code);
    if(success){ 
      // clear the search bar results via reference to object
      if (this.searchBarRef.current) {
        this.searchBarRef.current.value = "";
      }
      this.setState({ searchResults: []}, () => this.search());
    }
  }

  /**
   * Checks the term offerings of the element that changed.
   */
  handleCheckChanged(event: ChangeEvent<HTMLInputElement>) {
    var target = event.target;
    this.setState(state => {
      let filters = state.termFilters;
      filters[parseInt(target.name)] = target.checked;
      return {termFilters: filters};
    }, () => this.search());
  }

  /**
   * HTML output of search for courses.
   */
  render() {
    return (
      <CoursesContainer>
        <form>
          <CourseSearchBar
            ref={this.searchBarRef}
            placeholder="Search for a course..."
            onChange={this.handleInputChange}
          />
          <TermFilterGroup controlId="terms">
          Filter by Term:   
          {this.state.termFilters.map((checked, index) =>
            <TermFilter
              inline
              label={`${index + 1}`}
              name={`${index}`}
              checked={checked}
              key={`${index}`}
              type="checkbox"
              onChange={this.handleCheckChanged}
            />
          )}
          </TermFilterGroup>
        </form>
      {
        this.state.searchResults.length > 0 &&
        <CourseSuggestions 
          courses={this.state.searchResults} 
          add_event={this.addCourse}
        />
        }
      </CoursesContainer>
      )
  }
}

export { SearchCourses };
