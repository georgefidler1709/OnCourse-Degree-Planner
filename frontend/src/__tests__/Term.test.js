import React from 'react'
import { shallow, mount } from 'enzyme';
import { DragDropContext } from 'react-beautiful-dnd';
import Term from '../__components__/timeline_view/Term';

console.error = jest.fn();
console.warn = jest.fn();

describe("Won't render correctly outside of a DragDropContext", () => {
    it('renders correctly', () => {
      const wrapper = shallow(<Term 
                                  key="test" 
                                  termId="2 2019" 
                                  courses={[]}
                                  highlight={false} 
                                  removeCourse={(s) => {return}}
                                  getError={(s) => undefined}
                                  getWarn={(s) => undefined}
                                />);
      expect(wrapper).toMatchSnapshot();
    });

    it('Will render correctly within a DropDropContext', () => {
      const wrapper = mount(
      <DragDropContext>
      {
        <Term key="test" termId="2 2019" courses={[]}/>
      }
      </DragDropContext>);
      expect(wrapper).toMatchSnapshot();
    });

    it('Shows correct term title', () => {
      const wrapper = mount(
      <DragDropContext>
      {
        <Term key="test" termId="2 2019" courses={[]}/>
      }
      </DragDropContext>);
      expect(wrapper.find(Term).first().text()).toBe('T2 2019')
    });
});