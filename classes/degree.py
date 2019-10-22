"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degree.py
Implementation of the Degree class which is an object corresponding to a degree
offered by the university, and contains information about the degree completion
requirements.

[MORE INFO ABOUT CLASS]
"""

from typing import List

class Degree(object):

    def __init__(self, alphaCode: str, numCode: int, name: str, requirements: List[DegreeReq]):
        self._alphaCode = alphaCode
        self._numCode = numCode
        self._name = name
        self._requirements = requirements

    @property
    def alphaCode(self) -> str:
        return self._alphaCode

    @property
    def numCode(self) -> str:
        return self._numCode

    @property
    def name(self) -> str:
        return self._name


    # Input: either nothing or a list of completed courses (<List>CourseEnrollment)
    # Return: list of requirements remaining for completion
    def getRequirements(self, courses: List[CourseEnrollment]=None) -> List[DegreeReq]:
        # TODO
        pass

    # Input: list of courses completed
    # Return: boolean indicating whether degree completed
    def complete(self, courses: List[CourseEnrollment]) -> bool:
        # TODO
        # NOTE we might have to consider how to handle one course
        # fulfilling multiple requirements
        pass
