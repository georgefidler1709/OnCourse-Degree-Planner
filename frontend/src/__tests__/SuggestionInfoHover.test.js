import React from 'react'
import { shallow } from 'enzyme';
import SuggestionInfoHover from '../SuggestionInfoHover';

describe('Rendering the degree search page', () => {
    it('renders without crashing', () => {
      shallow(
        <SuggestionInfoHover
          content={<div>More Info</div>}
          placement="top"
          delay={200}
        >
          <div>Show tooltip</div>
        </SuggestionInfoHover>
      )
    });
});
