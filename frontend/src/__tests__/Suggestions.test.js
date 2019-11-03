import React from 'react'
import { shallow, mount } from 'enzyme';
import Suggestions from '../Suggestions';
import {API_ADDRESS} from '../Constants'

const mockDegrees = [{id: 1, code:"COMP3778", name: "Bachelor of Computer Science (2019)"}, {id: 2, code:"COMP3978", name: "Bachelor of Computer Science (2016)"}]

jest.mock("react-router-dom", () => ({
	useHistory: jest.fn(() => {
		return {
			push: jest.fn()
		}
	})
  }))

describe('Rendering a degree suggestion', () => {
    it('renders without crashing', () => {
      const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
	});

	it('puts the code of provided degrees as titles', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const id = wrapper.find('.suggestion-code').first().text();
		expect(id).toBe(mockDegrees[0].id.toString());
	})

	it('puts the course name of provided degrees underneath title', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const code = wrapper.find('.suggestion-name').first().text();
		expect(code).toBe(mockDegrees[0].name);
	})

	it('renders degree suggestions in the order they are provided', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const code1 = wrapper.find('.suggestion-code').first().text();
		expect(code1).toBe(mockDegrees[0].id.toString());
		const code2 = wrapper.find('.suggestion-code').at(1).text();
		expect(code2).toBe(mockDegrees[1].id.toString());
	})

	//Implement this test once this feature is up and running
	
	it('tells the backend the course code of a degree when a user selects it', () => {
		const fetchSpy = jest.spyOn(window, 'fetch');
		const component = mount(
			<Suggestions degrees={mockDegrees}/>
		);
		
		component.find('button.suggestion').first().simulate('click');
		expect(fetchSpy).toHaveBeenCalledWith(API_ADDRESS + "/" + mockDegrees[0].name);
		component.unmount();
		
	})	
});
