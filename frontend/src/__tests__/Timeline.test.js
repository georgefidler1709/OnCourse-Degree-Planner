import React from 'react'
import { shallow, mount } from 'enzyme';
import { Button } from 'react-bootstrap'
import Timeline from '../__components__/timeline_view/Timeline';

const mockLocation = {
  pathname: "/3778 COMPA1/2020"
} 

console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}


describe('savePlan method', () => {
  it('saves a plan when save button is pressed', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
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
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]
    let source_length = wrapper.state().program.enrollments[0].term_plans[0].course_ids.length
    let new_source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[1]

    wrapper.instance().onDragEnd({
      destination: {index: 2, droppableId: "1 2020"},
      source: {index: 0, droppableId: "1 2020"},
      draggableId: source_course,
    })

    await sleep(1000);
    wrapper.update()
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]).toBe(new_source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[2]).toBe(source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids.length).toBe(source_length)
  });

  it('will preserve changing the term of a course', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();
    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]
    let new_source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[1]
    let source_length = wrapper.state().program.enrollments[0].term_plans[0].course_ids.length
    let dest_length = wrapper.state().program.enrollments[0].term_plans[2].course_ids.length

    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "3 2020"},
      source: {index: 0, droppableId: "1 2020"},
      draggableId: source_course,
    })

    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]).toBe(new_source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids).toHaveLength(source_length - 1)
    expect(wrapper.state().program.enrollments[0].term_plans[2].course_ids[0]).toBe(source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[2].course_ids).toHaveLength(dest_length + 1)
  });

  it('will block overloading', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();
    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]
    let source_length = wrapper.state().program.enrollments[0].term_plans[0].course_ids.length

    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "2 2020"},
      source: {index: 0, droppableId: "1 2020"},
      draggableId: source_course,
    })

    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids[0]).toBe(source_course)
    expect(wrapper.state().program.enrollments[0].term_plans[0].course_ids).toHaveLength(source_length)
  });


  it('will block a course being dropped in a term it is not offered in', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    let source_course = wrapper.state().program.enrollments[1].term_plans[1].course_ids[0]
    let source_length = wrapper.state().program.enrollments[1].term_plans[1].course_ids.length

    expect(source_course).toBe("COMP3121");

    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "1 2021"},
      source: {index: 0, droppableId: "2 2021"},
      draggableId: source_course,
    })

    expect(wrapper.state().program.enrollments[1].term_plans[1].course_ids[0]).toBe(source_course)
    expect(wrapper.state().program.enrollments[1].term_plans[1].course_ids).toHaveLength(source_length)
  });

  it('will highlight a course being taken before prereqs are met', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    let source_course = wrapper.state().program.enrollments[0].term_plans[0].course_ids[1]
    let test_course = wrapper.state().program.enrollments[0].term_plans[1].course_ids[0]

    //COMP1511 is a prereq for COMP1521
    expect(source_course).toBe("COMP1511")
    expect(test_course).toBe("COMP1521")

    wrapper.instance().onDragEnd({
      destination: {index: 0, droppableId: "3 2020"},
      source: {index: 1, droppableId: "1 2020"},
      draggableId: source_course,
    })

    await sleep(100);
    wrapper.update();

    expect(wrapper.state().reqs.courses[test_course]).toBeTruthy()


    wrapper.instance().onDragEnd({
      destination: {index: 1, droppableId: "1 2020"},
      source: {index: 0, droppableId: "1 2020"},
      draggableId: source_course,
    })
    
  });


});

describe('addMissingTerms method', () => {
  it('will add missing term', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(1000);
    wrapper.update();
    wrapper.state().program.enrollments[0].term_plans.pop()
    expect(wrapper.state().program.enrollments[0].term_plans).toHaveLength(2)
    wrapper.instance().addMissingTerms()
    expect(wrapper.state().program.enrollments[0].term_plans).toHaveLength(3)
  });

  it('will add a missing year', async() => {
    const wrapper = shallow(<Timeline location={mockLocation} />);
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
    const wrapper = shallow(<Timeline location={mockLocation} />);
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
    const wrapper = shallow(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    expect(wrapper).toMatchSnapshot(); 

    wrapper.unmount();
  })
});


describe('add and remove years', () => {
  it('add an empty year', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    const original_years = wrapper.state().program.enrollments.length
    wrapper.instance().updateDuration(1)
    wrapper.update();
    const new_years = wrapper.state().program.enrollments.length
    expect(new_years).toBe(original_years + 1);

    wrapper.unmount();
  });

  it('remove an empty year', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();

    const original_years = wrapper.state().program.enrollments.length
    wrapper.instance().updateDuration(-1)
    wrapper.update();
    const new_years = wrapper.state().program.enrollments.length
    expect(new_years).toBe(original_years - 1);

    wrapper.unmount();
  });

  it('will not remove a year with courses in it', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().updateDuration(-1)
    wrapper.update();

    const original_years = wrapper.state().program.enrollments.length
    wrapper.instance().updateDuration(-1)
    wrapper.update();
    const new_years = wrapper.state().program.enrollments.length
    expect(new_years).toBe(original_years);

    wrapper.unmount();
  });
});


describe('removeCourse method', () => {
  it('has the course to be removed before removal', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();
    expect(wrapper.state().courses["COMP1511"]).toBeDefined()
  });

  it('does not have removed course after removal', async() => {
    const wrapper = mount(<Timeline location={mockLocation} />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().removeCourse("COMP1511")

    expect(wrapper.state().courses["COMP1511"]).toBeUndefined()
  });
});