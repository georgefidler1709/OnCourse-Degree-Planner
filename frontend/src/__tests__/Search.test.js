
import React from 'react'
import { shallow } from 'enzyme';
import Search from '../__components__/degree_search/Search';

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

describe('Rendering the degree search page', () => {
  it('renders correctly', async() => {
    const wrapper = shallow(<Search />);
    await sleep(100);
    wrapper.update();
    expect(wrapper).toMatchSnapshot(); 
  })

  it('shows a degrees with a names/coded with a substring the search bar input', async() => {
    const wrapper = shallow(<Search />);
    await sleep(100);
    wrapper.update();
    expect(wrapper.find('input')).toBe('f')//.simulate('keydown', { which: 'c' })
    wrapper.update()
    expect(wrapper.state()).toBe('f')
  })

  it('will send you to a timeline view for a given degree when you click on that degree', () => {
    

  })
});
