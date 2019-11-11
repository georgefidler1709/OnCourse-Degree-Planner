import React from 'react'
import { shallow, mount } from 'enzyme';
import Timeline from '../__components__/timeline_view/Timeline';
import InfoBar from '../__components__/timeline_view/InfoBar';

console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

const mockProgram = {
  degree_id: "3778",
  degree_name: "Computing",
  degree_reqs: [{filter_type: "GenEd", units: 12}, {filter_type: "FreeElective", units: 36}]
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('Render degree planning timeline view', () => {
  it('renders correctly', () => {
    <InfoBar 
      {...mockProgram}
    />
  })
  it('renders correctly as part of timeline', async() => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();
    expect(wrapper).toMatchSnapshot();
  });
});
