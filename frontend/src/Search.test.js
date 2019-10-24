import React from 'react'
import { shallow } from 'enzyme';
import Search from './Search';

describe('Rendering the degree search page', () => {
    it('renders without crashing', () => {
      shallow(<Search />);
    });

    const getDegrees = Search.prototype.getDegrees = jest.fn();
	const wrapper = shallow(<Search />);
    wrapper.find('input.search-bar').simulate("change", { target: { value: "foo" }})
    
    it('Keeps track of user input into the search field', () => {
		expect(wrapper.state('query')).toBe("foo")
	})

    it('Informs backend of users live input to give degree search suggestions', () => {
		expect(getDegrees).toHaveBeenCalled();
    })
});
