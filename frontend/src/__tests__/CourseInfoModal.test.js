import React from 'react'
import {  mount } from 'enzyme';
import CourseInfoModal from '../__components__/timeline_view/CourseInfoModal';
import Button from "react-bootstrap/Button";

const mockCourse = {
  key: "key",
  index: 0,
  code: "COMP3121",
  coreqs: "",
  equivalents: "COMP3821, COMP9801, COMP3120, COMP9101",
  exclusions: "",
  name: "Algorithms and Programming Techniques",
  prereqs: "(COMP1927 OR COMP2521)",
}


console.error = jest.fn();

let modalShow = true;
let setModalShow = jest.fn()
describe('Rendering a course info popup', () => {
  it('renders correctly', () => {
    const wrapper = mount(<CourseInfoModal
      show={modalShow}
      onHide={() => setModalShow(false)}
      {...mockCourse}
    />);
    expect(wrapper).toMatchSnapshot();

    wrapper.unmount();
  });

  it('will be removed when close button clicked', () => {
      const wrapper = mount(<CourseInfoModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        {...mockCourse}
      />);
      
      wrapper.find(Button).first().simulate('click');
      expect(setModalShow).toHaveBeenCalledWith(false);

      wrapper.unmount();
    });

    it('display reqs correctly', () => {
      const wrapper = mount(<CourseInfoModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        {...mockCourse}
      />);
      //enzyme does not include html to the line break between : and COMP1927 is preserved
      expect(wrapper.find("#Prereqs").text()).toBe('Prereqs:COMP1927 OR COMP2521')
      wrapper.unmount();
    });
});