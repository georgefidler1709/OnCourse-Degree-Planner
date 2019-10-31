"""
COMP4290 Group Project
Team: On Coursee
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

generator.py
A generator which creates a degree plan for a given degree

[MORE INFO ABOUT CLASS]
"""

from . import degree
from . import program
from . import university

class Generator(object):

    def __init__(self, degree: 'degree.Degree', university: 'university.University'):
        self.degree = degree
        self.term_unit_cap = 18 # default for first release

    def generate(self):
        program = program.Program(self.degree, [])
        for req in degree.requirements:
            while not req.fulfilled(program):
                pass
                # add a new subject





