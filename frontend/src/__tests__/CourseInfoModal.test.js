import React from 'react'
import {  mount } from 'enzyme';
import CourseInfoModal from '../__components__/timeline_view/CourseInfoModal';
import Button from "react-bootstrap/Button";

console.error = jest.fn();

let modalShow = true;
let setModalShow = jest.fn()
describe('Rendering a course info popup', () => {
  it('renders correctly', () => {
    const wrapper = mount(<CourseInfoModal
      show={modalShow}
      onHide={() => setModalShow(false)}
      courseId={"COMP1511"}
      course={{}}
    />);
    expect(wrapper).toMatchSnapshot();

    wrapper.unmount();
  });

  it('will be removed when close button clicked', () => {
      const wrapper = mount(<CourseInfoModal
        show={modalShow}
        onHide={() => setModalShow(false)}
        courseId={"COMP1511"}
        course={{}}
      />);
      
      wrapper.find(Button).first().simulate('click');
      expect(setModalShow).toHaveBeenCalledWith(false);

      wrapper.unmount();
    });
});