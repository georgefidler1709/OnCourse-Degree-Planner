import React from 'react'
import { shallow } from 'enzyme';
import Search from './Search';

const mockDegrees = [{id: 1, code:"COMP3778", name: "Bachelor of Computer Science (2019)"}, {id: 2, code:"COMP3978", name: "Bachelor of Computer Science (2016)"}]

describe('Rendering the degree search page', () => {
    it('renders without crashing', () => {
      shallow(<Search />);
    });
    
    
	
});
