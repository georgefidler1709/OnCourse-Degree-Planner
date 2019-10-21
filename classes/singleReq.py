"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

singleReq.py
A single course requirement
Abstract class which collects the different types of single course requirement

[MORE INFO ABOUT CLASS]
"""

from abc import ABC

class SingleReq(CourseReq, ABC):
    
    def __init__(self):
        super().__init__()

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    @abstractmethod
    def fulfilled(self, program, term, coreq=false):
        pass

