import React from 'react'
import { shallow, mount } from 'enzyme';
import CourseDropBox from '../__components__/timeline_view/CourseDropBox';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';

console.error = jest.fn();

describe('Render degree planning timeline view', () => {
  it('renders correctly', () => {
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
                <CourseDropBox type="test"/>
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
});
