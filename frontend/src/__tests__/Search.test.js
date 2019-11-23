
import React from 'react'
import { shallow, mount } from 'enzyme';
import Search from '../__components__/degree_search/Search';
import {Dropdown} from 'react-bootstrap'

console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('Rendering the degree search page', () => {
  it('renders correctly', async() => {
    const wrapper = shallow(<Search />);
    await sleep(100);
    wrapper.update();
    expect(wrapper).toMatchSnapshot(); 
  })

  it('shows a degrees with a names/coded with a substring the search bar input', async() => {
    const wrapper = shallow(<Search />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().handleInputChange({target: {value: 'c'}})
    wrapper.update()
    expect(wrapper.state().searchResults.findIndex(res => res.degree.name === "Computer Science") !== -1).toBeTruthy();
  });

  it('will let you select the starting year of your degree', async() => {
    const wrapper = shallow(<Search />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().setYear(2021);
    expect(wrapper.html().indexOf("Start Year: 2021")).toBeTruthy()

  })
});
