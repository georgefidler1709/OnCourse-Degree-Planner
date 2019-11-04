import React from 'react'
import { shallow } from 'enzyme';
import Search from '../__components__/degree_search/Search';

describe('Rendering the degree search page', () => {
    it('renders correctly', () => {
      const wrapper = shallow(<Search />);
      expect(wrapper).toMatchSnapshot();
    });
    
    const getDegrees = Search.prototype.getDegrees = jest.fn();
	  const wrapper = shallow(<Search />);
    wrapper.find('input.search-bar').simulate("change", { target: { value: "foo" }})
    
    it('Keeps track of user input into the search field', () => {
		expect(wrapper.state('query')).toBe("foo")
	});

    it('Informs backend of users live input to give degree search suggestions', () => {
		expect(getDegrees).toHaveBeenCalled();
    });
});
