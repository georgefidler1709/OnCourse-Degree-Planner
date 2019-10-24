import React from 'react'
import { shallow } from 'enzyme';
import Suggestions from './Suggestions';

const mockDegrees = [{id: 1, code:"COMP3778", name: "Bachelor of Computer Science (2019)"}, {id: 2, code:"COMP3978", name: "Bachelor of Computer Science (2016)"}]

describe('Rendering a degree suggestion', () => {
    it('renders without crashing', () => {
      shallow(<Suggestions degrees={mockDegrees}/>);
	});

	it('puts the code of provided degrees as titles', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const code = wrapper.find('.suggestion-code').first().text();
		expect(code).toBe(mockDegrees[0].code);
	})

	it('puts the course name of provided degrees underneath title', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const code = wrapper.find('.suggestion-name').first().text();
		expect(code).toBe(mockDegrees[0].name);
	})

	it('renders degree suggestions in the order they are provided', () => {
		const wrapper = shallow(<Suggestions degrees={mockDegrees}/>);
		const code1 = wrapper.find('.suggestion-code').first().text();
		expect(code1).toBe(mockDegrees[0].code);
		const code2 = wrapper.find('.suggestion-code').at(1).text();
		expect(code2).toBe(mockDegrees[1].code);
	})

	//Implement this test once this feature is up and running
	//
	//const mockAPICall = jest.fn();
	// it('tells the backend the course code of a degree when a user selects it', () => {
	// 	const component = mount(
	// 		<Suggestions degrees={mockDegrees}/>
	// 	);
	// 	component.find('button.suggestion').first().simulate('click');
	// 	expect(mockAPICall).toHaveBeenCalledWith(mockDegrees[0].code);
		
	// 	component.unmount();
	// })
	
});
