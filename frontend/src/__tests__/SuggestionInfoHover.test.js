import React from 'react'
import { shallow} from 'enzyme';
import SuggestionInfoHover from '../__components__/degree_search/SuggestionInfoHover';
import { Popover } from 'react-bootstrap'


describe('Rendering a degree tooltip', () => {
    it('renders correctly', () => {
      let wrapper = shallow(
        <SuggestionInfoHover
          content={<div>More Info</div>}
          placement="top"
          delay={200}
        >
          <div className="test">Show tooltip</div>
        </SuggestionInfoHover>
      )
      expect(wrapper).toMatchSnapshot();
    });

    it('displays more info on mouseover', () => {
      let wrapper = shallow(
        <SuggestionInfoHover
          content={<div>More Info</div>}
          placement="top"
          delay={200}
        >
          <div className="test">Show tooltip</div>
        </SuggestionInfoHover>
      )

      wrapper.find('.test').simulate('mouseover');
      wrapper.update();

      expect(wrapper.find(Popover.Content).text()).toBe('More Info')
      expect(wrapper).toMatchSnapshot();
    });


});
