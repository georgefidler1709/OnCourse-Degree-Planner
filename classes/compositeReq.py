"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

compositeReq.py
A composite course requirement, where more than one requirement must be considered
Abstract class which collects the two kinds of composite requirement (AND/OR)

[MORE INFO ABOUT CLASS]
"""

from abc import abc

class CompositeReq(CourseReq, ABC):
    
    def __init__(self, reqs):
        super().__init__()
        self.reqs = reqs # <List>CourseReq

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    @abstractmethod
    def fulfilled(self, program, term, coreq=false):
        pass
