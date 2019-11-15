import React from 'react'
import { shallow, mount } from 'enzyme';
import { Button } from 'react-bootstrap'
import Timeline from '../__components__/timeline_view/Timeline';
import InfoBar from '../__components__/timeline_view/InfoBar';

console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('savePlan method', () => {
  it('saves a plan when save button is pressed', async() => {
    const wrapper = mount(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(100);
    wrapper.update();

    const instance = wrapper.instance();
    instance.savePlan = jest.fn()
    const spy = jest.spyOn(instance, 'savePlan');
    wrapper.instance().forceUpdate();
    wrapper.find(Button).first().simulate('click');
    expect(spy).toHaveBeenCalled();

    wrapper.unmount();
  });
});

describe('onDragEnd method', () => {
  it('will preserve changing of the order of courses within a term', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();

    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]
    let source_length = wrapper.state().program.enrollments[0].term_plans[0].course_ids.length
    let new_source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[1]

    wrapper.instance().onDragEnd({
      destination: {index: 2, droppableId: "1 2019"},
      source: {index: 0, droppableId: "1 2019"},
      draggableId: source_course,
    })
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]).toBe(new_source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[2]).toBe(source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids.length).toBe(source_length)
  });
  it('will preserve changing the term of a course', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();
    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]
    let new_source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[1]
    let source_length = wrapper.state().program.enrollments[0].term_plans[0].course_ids.length
    let dest_length = wrapper.state().program.enrollments[0].term_plans[1].course_ids.length

    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "2 2019"},
      source: {index: 0, droppableId: "1 2019"},
      draggableId: source_course,
    })
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]).toBe(new_source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids).toHaveLength(source_length - 1)
    expect(wrapper.state().program.enrollments[0].term_plans[1].course_ids[0]).toBe(source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[1].course_ids).toHaveLength(dest_length + 1)

    // reverse operation
    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "1 2019"},
      source: {index: 0, droppableId: "2 2019"},
      draggableId: "COMP1511",
    })
  });
});

describe('addMissingTerms method', () => {
  it('will add missing term', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();
    wrapper.state().program.enrollments[0].term_plans.pop()
    expect(wrapper.state().program.enrollments[0].term_plans).toHaveLength(2)
    wrapper.instance().addMissingTerms()
    expect(wrapper.state().program.enrollments[0].term_plans).toHaveLength(3)
  });

  it('will add a missing year', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();
    wrapper.state().program.enrollments.pop()
    expect(wrapper.state().program.enrollments).toHaveLength(2)
    wrapper.instance().addMissingTerms()
    expect(wrapper.state().program.enrollments).toHaveLength(3)
  });
});

describe('onDragStart method', () => {
  it('will highlight terms which contain an offering for the course being dragged', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(100);
    wrapper.update();

    wrapper.instance().onDragStart({draggableId: "COMP3121", source: {droppableId: "1 2019"}})
    expect(wrapper.state().program.enrollments[0].term_plans[0].highlight).toBeFalsy()
    await sleep(100);
    wrapper.update();
    expect(wrapper.state().program.enrollments[0].term_plans[1].highlight).toBeTruthy()
  });
});

describe('Render degree planning timeline view', () => {
  it('renders correctly', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(100);
    wrapper.update();

    expect(wrapper).toMatchSnapshot(); 

    wrapper.unmount();
  })
});

describe('removeCourse method', () => {
  it('has the course to be removed before removal', async() => {
    const wrapper = mount(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(100);
    wrapper.update();
    expect(wrapper.state().courses["COMP1511"]).toBeDefined()
  });

  it('does not have removed course after removal', async() => {
    const wrapper = mount(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().removeCourse("COMP1511")
    expect(wrapper.state().courses["COMP1511"]).toBeUndefined()
  });
});