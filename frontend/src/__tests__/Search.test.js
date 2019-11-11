import fetch, {Response} from 'node-fetch';
import React from 'react'
import { shallow } from 'enzyme';
import Search from '../__components__/degree_search/Search';

describe('Rendering the degree search page', () => {
  fetch.mockReturnValue(
    Promise.resolve(
      new Response(`
        [
          { id: "1", name: "this is a test" },
          { id: "2", name: "blah" },
          { id: "3", name: "foo bar" },
          { id: "4", name: "tea" },
        ] `
      )
    )
  );

  const wrapper = shallow(<Search />);
  
  it('renders correctly', () => {
    expect(wrapper).toMatchSnapshot();
  });

  it('searches correctly', () => {
    expect(wrapper.state.degrees).toEqual([{ id: "1", name: "this is a test" }]);
  });
});
