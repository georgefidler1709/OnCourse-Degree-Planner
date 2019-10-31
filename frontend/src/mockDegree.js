const mockDegree = {
  courses: {
    'course-1': { id: 'course-1', content: 'COMP1511' },
    'course-2': { id: 'course-2', content: 'MATH1131' },
    'course-3': { id: 'course-3', content: 'MATH1081' },
    'course-4': { id: 'course-4', content: 'COMP1521' },
    'course-5': { id: 'course-5', content: 'MATH1231' },
    'course-6': { id: 'course-6', content: 'COMP1531' },
    'course-7': { id: 'course-7', content: 'COMP2521' },
    'course-8': { id: 'course-8', content: 'COMP2511' },
    'course-9': { id: 'course-9', content: 'COMP3121' },
    'course-10': { id: 'course-10', content: 'COMP4920' },
  },

  terms: {
    'term-1': {
      id: 'term-1',
      title: 'T1 2019',
      courseIds: ['course-1', 'course-2', 'course-3'],
    },
    'term-2': {
      id: 'term-2',
      title: 'T2 2019',
      courseIds: ['course-4'],
    },
    'term-3': {
      id: 'term-3',
      title: 'T3 2019',
      courseIds: ['course-5', 'course-6'],
    },
    'term-4': {
      id: 'term-4',
      title: 'T1 2020',
      courseIds: ['course-7'],
    },
    'term-5': {
      id: 'term-5',
      title: 'T2 2020',
      courseIds: [],
    },
    'term-6': {
      id: 'term-6',
      title: 'T3 2020',
      courseIds: ['course-8', 'course-9'],
    },
    'term-7': {
      id: 'term-7',
      title: 'T1 2021',
      courseIds: ['course-10'],
    },
    'term-8': {
      id: 'term-8',
      title: 'T2 2021',
      courseIds: [],
    },
    'term-9': {
      id: 'term-9',
      title: 'T3 2021',
      courseIds: [],
    },
  },

  years: {
    '2019': { 
      id: '2019', 
      termOrder: ['term-1', 'term-2', 'term-3'],
    },
    '2020': { 
      id: '2020', 
      termOrder: ['term-4', 'term-5', 'term-6'],
    },
    '2021': { 
      id: '2021', 
      termOrder: ['term-7', 'term-8', 'term-9'],
    },
  }, 

  yearOrder: ['2019', '2020', '2021']

};
  
  export default mockDegree;
