import React from 'react'
import { shallow } from 'enzyme';
import Suggestions from '../__components__/degree_search/Suggestions';

const mockSearchResults = {
	degrees: 
	[{
        code: "3502 ACCTA1",
        degree: { 
            id: "3502 ACCTA1",
            name: "Commerce (Accounting)",
            years: [2020, 2021]
        },
        text: "Commerce (Accounting)"
    },
    {
        code: "3778 COMPA1",
        degree: { 
            id: "3778 COMPA1",
            name: "Computer Science",
            years: [2020, 2021]
        },
        text: "Computer Science"
    }], 
	year: 2020
}

console.warn = jest.fn();

jest.mock("react-router-dom", () => ({
	useHistory: jest.fn(() => {
		return {
			push: jest.fn()
		}
	})
  }))

describe('Rendering a degree suggestion', () => {
    it('renders correctly', () => {
	  const wrapper = shallow(<Suggestions {...mockSearchResults}/>);
	  expect(wrapper).toMatchSnapshot();
	});

	it('puts the code of provided degrees as titles', () => {
		const wrapper = shallow(<Suggestions {...mockSearchResults}/>);
		
		expect(wrapper.html().includes(">3778 COMPA1</h1>")).toBeTruthy()
	})

	it('renders degree suggestions in the order they are provided', () => {
		const wrapper = shallow(<Suggestions {...mockSearchResults}/>);
		const code1 = wrapper.html().indexOf(">3502 ACCTA1</h1>")
		const code2 = wrapper.html().indexOf(">3778 COMPA1</h1>")
		expect(code1 < code2).toBeTruthy();
	})	
});
