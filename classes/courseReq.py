"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

courseReq.py
Implementation of the CourseReq class, an abstract class which collects types
of course requirements.

[MORE INFO ABOUT CLASS]
"""

from abc import ABC

class CourseReq(ABC):

    def __init__(self):
        pass

    # Input: Program of study, term this course is to be taken
    # Return: Whether this requirement is fulfilled
    # coreq set to false, if true then terms allowed include input term
    @abstractmethod
    def fulfilled(self, program, term, coreq=false):
        pass