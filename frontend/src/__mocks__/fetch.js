import {API_ADDRESS} from '../Constants'
import { mockPlan } from 'mockPlan'

export default function fetch(type){
  if(type === API_ADDRESS + `/degree/gen_program.json`) return Promise.resolve({json: () => {
    return {...mockPlan}
  }})
}
