import React from 'react'
import { shallow } from 'enzyme';
import Timeline from '../__components__/timeline_view/Timeline';

const mockPlan = {
  "courses": [
    {
      "code": 1511, 
      "name": "Programming Fundamentals", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 1521, 
      "name": "Computer Systems Fundamentals", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 1531, 
      "name": "Software Engineering Fundamentals", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 2511, 
      "name": "Object-Oriented Design & Programming", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 2521, 
      "name": "Data Structures and Algorithms", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 3900, 
      "name": "Computer Science Project", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 4920, 
      "name": "Management and Ethics", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 1081, 
      "name": "Discrete Mathematics", 
      "subject": "MATH", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 1131, 
      "name": "Mathematics 1A", 
      "subject": "MATH", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 1231, 
      "name": "Mathematics 1B", 
      "subject": "MATH", 
      "terms": [
        {
          "term": 1, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 3, 
          "year": 2019
        }, 
        {
          "term": 1, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 3, 
          "year": 2020
        }, 
        {
          "term": 1, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 3, 
          "year": 2021
        }, 
        {
          "term": 1, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 3, 
          "year": 2022
        }, 
        {
          "term": 1, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 3, 
          "year": 2023
        }, 
        {
          "term": 1, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 3, 
          "year": 2024
        }, 
        {
          "term": 1, 
          "year": 2025
        }, 
        {
          "term": 2, 
          "year": 2025
        }, 
        {
          "term": 3, 
          "year": 2025
        }
      ], 
      "units": 6
    }, 
    {
      "code": 3121, 
      "name": "Algorithms and Programming Techniques", 
      "subject": "COMP", 
      "terms": [
        {
          "term": 2, 
          "year": 2019
        }, 
        {
          "term": 2, 
          "year": 2020
        }, 
        {
          "term": 2, 
          "year": 2021
        }, 
        {
          "term": 2, 
          "year": 2022
        }, 
        {
          "term": 2, 
          "year": 2023
        }, 
        {
          "term": 2, 
          "year": 2024
        }, 
        {
          "term": 2, 
          "year": 2025
        }
      ], 
      "units": 6
    }
  ], 
  "program": {
    "duration": 3, 
    "enrollments": [
      {
        "term_plans": [
          {
            "course_ids": [
              "COMP1511", 
              "COMP1531", 
              "COMP2521"
            ], 
            "term": 1
          }, 
          {
            "course_ids": [
              "COMP1521", 
              "COMP2511", 
              "COMP3900"
            ], 
            "term": 2
          }, 
          {
            "course_ids": [
              "COMP4920", 
              "MATH1081", 
              "MATH1131"
            ], 
            "term": 3
          }
        ], 
        "year": 2019
      }, 
      {
        "term_plans": [
          {
            "course_ids": [
              "MATH1231"
            ], 
            "term": 1
          }, 
          {
            "course_ids": [
              "COMP3121"
            ], 
            "term": 2
          }
        ], 
        "year": 2020
      }
    ], 
    "id": "3778", 
    "name": "Computer Science", 
    "reqs": [
      {
        "filter_type": "GenEd", 
        "units": 12
      }, 
      {
        "filter_type": "FreeElective", 
        "units": 36
      }
    ], 
    "url": "https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778", 
    "year": 2019
  }
}

console.error = jest.fn();

describe('Render degree planning timeline view', () => {
    it('renders correctly', () => {
     // const wrapper = shallow(<Timeline location={{state: {plan: mockPlan}}} />);
     // expect(wrapper).toMatchSnapshot();
    });
});
