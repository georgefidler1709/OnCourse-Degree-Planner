import React from 'react'
import { shallow, mount } from 'enzyme';
import Suggestions from '../__components__/degree_search/Suggestions';

console.warn = jest.fn();

const mockDegrees = [
	{ degree: {
	  "id": "3778", 
	  "name": "Computer Science"
	} }, 
	{ degree: {
	  "id": "7001", 
	  "name": "Science"
	} }, 
  ]

jest.mock("react-router-dom", () => ({
	useHistory: jest.fn(() => {
		return {
			push: jest.fn()
		}
	})
  }))

describe('Rendering a degree suggestion', () => {
    it('renders correctly', () => {
	  const wrapper = shallow(<Suggestions degrees={mockDegrees} year={2020} />);
	  expect(wrapper).toMatchSnapshot();
	});

	it('puts the code of provided degrees as titles', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees} year={2020}/>);
		
		expect(wrapper.html().includes(">3778</h1>")).toBeTruthy()
	})

	it('renders degree suggestions in the order they are provided', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees} year={2020}/>);
		const code1 = wrapper.html().indexOf(">3778 COMPA1</h1>")
		const code2 = wrapper.html().indexOf(">3707 SENGAH</h1>")
		expect(wrapper.html()).toBe('f');
	})	
});
