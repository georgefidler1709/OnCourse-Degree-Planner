import {API_ADDRESS} from '../Constants'
import {mockPlan} from 'mockPlan'
import {mockCourse} from 'mockCourse'

export default function fetch(type) {
  if(type === API_ADDRESS + `/3778/gen_program.json`) return Promise.resolve({json: () => {
    return {...mockPlan}
  }})
  if(type === API_ADDRESS + `/COMP1511/course_info.json`) return Promise.resolve({json: () => {
    return mockCourse;
  }})
  else if(type === API_ADDRESS + `/full_courses.json`) return Promise.resolve({json: () => {
    return []
  }})
  else if(type instanceof Request && type.url === API_ADDRESS + '/check_program.json') return Promise.resolve({json: () => {
    return {...mockPlan}
  }})
}
