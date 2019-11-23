import React from 'react'
import { shallow, mount } from 'enzyme';
import Term from '../__components__/timeline_view/Term';
import Course from '../__components__/timeline_view/Course';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';

const mockCourse = {
  code: "COMP1511", 
  coreqs: "",
  equivalents: "",
  exclusions: "DPST1091",
  name: "Programming Fundamentals",
  prereqs: "",
}

console.error = jest.fn();
console.warn = jest.fn();
console.log = jest.fn();

describe('Rendering a course on the timeline', () => {
    it('draggable cannot render outside of a droppable', () => {
      const wrapper = shallow(<Course {...mockCourse} key={"COMP1511"} index={1} />);
      expect(wrapper).toMatchSnapshot();
    });

    it('renders correctly within a DragDropContext', () => {
      const wrapper = mount(
          <DragDropContext>
          {
           <Droppable droppableId="droppable">
           {(provided, snapshot) => (
             <div 
               innerRef={provided.innerRef} 
               {...provided.droppableProps}
             >
               {
                  <Course {...mockCourse}/>
               }
               {provided.placeholder}
             </div>
           )}
         </Droppable>
          }
          </DragDropContext>
          );
          expect(wrapper).toMatchSnapshot();
          
          wrapper.unmount();
    })

    it('can render correctly within a term', () => {
      const wrapper = mount(
      <DragDropContext>
      {
       <Term 
          key="test" 
          termId="term" 
          courses={[mockCourse]}
          highlight={false} 
          removeCourse={(s) => {return}}
          getError={(s) => undefined}
          getWarn={(s) => undefined}
        />
      }
      </DragDropContext>
      );
      expect(wrapper).toMatchSnapshot();
      
      wrapper.unmount();
    });

    it('shows correct course code', () => {
      const wrapper = mount(
      <DragDropContext>
      {
        <Term 
          key="test" 
          termId="term" 
          courses={[mockCourse]}
          highlight={false} 
          removeCourse={(s) => {return}}
          getError={(s) => undefined}
          getWarn={(s) => undefined}
        />
      }
      </DragDropContext>
      );
      expect(wrapper.find(Course).first().text()).toBe('COMP1511')
      
      wrapper.unmount();
    });
});