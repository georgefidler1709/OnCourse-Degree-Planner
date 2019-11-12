import {API_ADDRESS} from '../Constants'
import {mockPlan} from 'mockPlan'
import {mockDegrees} from 'mockDegrees'

export default function fetch(type){
  if(type === API_ADDRESS + `/degree/gen_program.json`) return Promise.resolve({json: () => mockPlan})
  if(type === API_ADDRESS + `/degrees.json`) return Promise.resolve({json: () => mockDegrees})
}
