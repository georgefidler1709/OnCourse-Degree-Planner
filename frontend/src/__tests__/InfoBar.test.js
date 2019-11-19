import React from 'react'
import { shallow, mount } from 'enzyme';
import Timeline from '../__components__/timeline_view/Timeline';
import InfoBar from '../__components__/timeline_view/InfoBar';
import CourseDropBox from '../__components__/timeline_view/CourseDropBox';
import { DragDropContext } from 'react-beautiful-dnd';
import { Card, Collapse } from 'react-bootstrap'


console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

const mockProgram = {
  degree_id: "3778",
  degree_name: "Computing",
  degree_reqs: [{filter_type: "GenEd", units: 12}, {filter_type: "FreeElective", units: 36}]
}

const mockCourse = {
  "code": "COMP1511", 
  "coreqs": "", 
  "equivalents": "", 
  "exclusions": "DPST1091", 
  "name": "Programming Fundamentals", 
  "prereqs": "", 
  "terms": [
    {
      "term": 1, 
      "year": 2019
    }, 
    {
      "term": 2, 
      "year": 2019
    }, 
    {
      "term": 3, 
      "year": 2019
    }, 
    {
      "term": 1, 
      "year": 2020
    }, 
    {
      "term": 2, 
      "year": 2020
    }, 
    {
      "term": 3, 
      "year": 2020
    }, 
    {
      "term": 1, 
      "year": 2021
    }, 
    {
      "term": 2, 
      "year": 2021
    }, 
    {
      "term": 3, 
      "year": 2021
    }, 
    {
      "term": 1, 
      "year": 2022
    }, 
    {
      "term": 2, 
      "year": 2022
    }, 
    {
      "term": 3, 
      "year": 2022
    }, 
    {
      "term": 1, 
      "year": 2023
    }, 
    {
      "term": 2, 
      "year": 2023
    }, 
    {
      "term": 3, 
      "year": 2023
    }, 
    {
      "term": 1, 
      "year": 2024
    }, 
    {
      "term": 2, 
      "year": 2024
    }, 
    {
      "term": 3, 
      "year": 2024
    }, 
    {
      "term": 1, 
      "year": 2025
    }, 
    {
      "term": 2, 
      "year": 2025
    }, 
    {
      "term": 3, 
      "year": 2025
    }
  ], 
  "units": 6
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
    wrapper.instance().addCourse(mockCourse, {}, [])
    await sleep(100);
    wrapper.update();
    expect(wrapper.find(InfoBar).find(CourseDropBox).props().add_course).toBe(mockCourse)
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
       />
      }
      </DragDropContext>);
    wrapper.find(InfoBar).find(Card.Header).at(1).simulate('click')
    expect(wrapper.find(InfoBar).find(Card.Header).at(1).props()["aria-expanded"]).toBeTruthy()
    expect(wrapper).toMatchSnapshot();
  })
})
