"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

generator.py
A generator which creates a degree plan for a given degree

[MORE INFO ABOUT CLASS]
"""

import program

class Generator(object):

    def __init__(self, degree: 'degree.Degree'):
        self.degree = degree
        self.term_unit_cap = 18 # default for first release
    
    def generate(self, university: 'university.University'):
        program = program.Program(self.degree, [])
        for req in degree.requirements:
            if isinstance(req, SpecificCourseFilter):
                while not req.fulfilled(program):
                    courses = university.filter_courses(req.filter)
                    

            else if isinstance(req, OrFilter):



                # add a new subject





