import React from 'react'
import { shallow, mount } from 'enzyme';
import Timeline from '../__components__/timeline_view/Timeline';
import InfoBar from '../__components__/timeline_view/InfoBar';
import InfoBarDropBox from '../__components__/timeline_view/InfoBarDropBox';
import { DragDropContext } from 'react-beautiful-dnd';
import { Card, Collapse } from 'react-bootstrap'
import mockCourse from '../__mocks__/mockCourse';


console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

const mockProgram = {
  degree_id: "3778",
  degree_name: "Computing",
  degree_reqs: [{filter_type: "GenEd", units: 12}, {filter_type: "FreeElective", units: 36}],
  standby_courses: [],
  done_courses: [],
}

const mockRoute = {
  params: {
    degree: "3778",
    reqs: undefined,
  }
} 


function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('Render degree planning timeline view', () => {
  it('renders correctly', () => {
    const wrapper = mount(
      <DragDropContext>
      {
       <InfoBar 
        {...mockProgram}
       />
      }
      </DragDropContext>);
      expect(wrapper).toMatchSnapshot();

      wrapper.unmount();
  })
  it('renders correctly as part of timeline', async() => {
    const wrapper = shallow(<Timeline match={mockRoute} />);
    await sleep(1000);
    wrapper.update();
    expect(wrapper).toMatchSnapshot();

    wrapper.unmount();
  });

  it('displays missing course under requirements if a required course is missing', async() => {
    const wrapper = mount(<Timeline match={mockRoute} />);
    await sleep(1000);
    wrapper.update();
    wrapper.instance().removeCourse("COMP1511");
    expect(wrapper.state().courses["COMP1511"]).toBeUndefined()
    expect(wrapper).toMatchSnapshot();

    wrapper.unmount();

  });

  it('adds a course to the Add box after search', async() => {
    const wrapper = mount(<Timeline match={mockRoute} />);
    await sleep(100);
    wrapper.update();
    wrapper.instance().addCourse("COMP1511")
    await sleep(100);
    wrapper.update();
    expect(wrapper.find(InfoBar).find(InfoBarDropBox).first().props().courses).toContain(mockCourse)
    expect(wrapper).toMatchSnapshot();

    wrapper.unmount();
  });
});

describe('Has collapsable sections', () => {
  it('can collapse a section', async() => {
    const wrapper = mount(
      <DragDropContext>
      {
       <InfoBar 
        {...mockProgram}
        add_course={undefined}
        add_event={jest.fn()}
        remove_course={jest.fn()}
       />
      }
      </DragDropContext>);
    wrapper.find(Card.Header).at(0).simulate('click')
    await sleep(1000);
    wrapper.update();
    expect(wrapper.find(Card.Header).at(0).props()["aria-expanded"]).toBeFalsy()
    expect(wrapper).toMatchSnapshot();
  })

  it('can expand a section', async() => {
    const wrapper = mount(
      <DragDropContext>
      {
       <InfoBar 
        {...mockProgram}
        add_course={undefined}
        add_event={jest.fn()}
        remove_course={jest.fn()}
        standby_course
       />
      }
      </DragDropContext>);
    wrapper.find(InfoBar).find(Card.Header).at(2).simulate('click');
    await sleep(1000);
    wrapper.update();
    expect(wrapper.find(InfoBar).find(Card.Header).at(2).props()["aria-expanded"]).toBeTruthy()
    expect(wrapper).toMatchSnapshot();
  })
})
