import React from 'react'
import { shallow } from 'enzyme';
import Term from '../__components__/timeline_view/Term';


describe('Rendering a term on the timeline', () => {
    it('renders correctly', () => {
      const wrapper = shallow(<Term key={"T2 2019"} termId={"T2 2019"} courses={[{subject: "COMP", code: "1511"}]} />);
      expect(wrapper).toMatchSnapshot();
    });
});