import json;

"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

apiTypes.py
Contains the json layout of the types to be sent over to the front end
"""

from typing import List
from typing_extensions import TypedDict

class SimpleDegree(TypedDict):
    id: int;
    name: str;

SimpleDegrees = List[SimpleDegree]
