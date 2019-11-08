import React from 'react'
import { shallow } from 'enzyme';
import Course from '../__components__/timeline_view/Course';

describe('Rendering a course on the timeline', () => {
    it('renders correctly', () => {
      const wrapper = shallow(<Course key={"COMP1511"} courseId={"COMP1511"} course={{}} index={1} />);
      expect(wrapper).toMatchSnapshot();
    });
});