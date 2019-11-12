import fetch, {Response} from 'node-fetch';
import Button from "react-bootstrap/Button";
import React from 'react'
import { shallow } from 'enzyme';
import Search from '../__components__/degree_search/Search';

describe('Rendering the degree search page', () => {

  const wrapper = shallow(<Search />);
  
  it('renders correctly', () => {
    expect(wrapper).toMatchSnapshot();
  });

  // TODO(kevin): fix these tests
  //wrapper.find('input.search-bar').simulate("change", { target: { value: "study" }})

  //it('searches correctly', () => {
  //  expect(wrapper.find(Button).first().text()).toBe("studyology");
  //});
});
