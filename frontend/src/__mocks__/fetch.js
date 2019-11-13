import {API_ADDRESS} from '../Constants'
import {mockPlan} from 'mockPlan'

export default function fetch(type) {
  console.log(type)
  if(type === API_ADDRESS + `/degree/gen_program.json`) return Promise.resolve({json: () => {
    return {...mockPlan}
  }})
  else if(type === API_ADDRESS + `/full_courses.json`) return Promise.resolve({json: () => {
    return []
  }})
  else if(type instanceof Request && type.url === API_ADDRESS + '/check_program.json') return Promise.resolve({json: () => {
    return {...mockPlan}
  }})
}
