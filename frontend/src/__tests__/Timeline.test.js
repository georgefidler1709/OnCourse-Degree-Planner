import React from 'react'
import { shallow, mount } from 'enzyme';
import Timeline from '../__components__/timeline_view/Timeline';
import Button from "react-bootstrap/Button";

console.error = jest.fn();

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('Render degree planning timeline view', () => {
  it('renders correctly', () => {
    const wrapper = shallow(<Timeline match={{params: {degree: "degree"}}} />);
    expect(wrapper).toMatchSnapshot();
  });

  it('saves a plan when save button is pressed', async() => {
    const wrapper = mount(<Timeline match={{params: {degree: "degree"}}} />);
    await sleep(1000);
    wrapper.update();

    const instance = wrapper.instance();
    const spy = jest.spyOn(instance, 'savePlan');
    wrapper.instance().forceUpdate();
    wrapper.find(Button).first().simulate('click');
    expect(spy).toHaveBeenCalled();

    wrapper.unmount();
  });

});
