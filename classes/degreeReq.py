"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

degreeReq.py
Implementation of the DegreeReq class which specifies a degree requirement.
These requirements take the form of a count of units from a particular
filter of courses.

[MORE INFO ABOUT CLASS]
"""


from university import University

class DegreeReq(object):

    def __init__(self):
        # input as separate variables? or some other format
        # self.units =
        # self.filter =
        super().__init__()

    # check list of courses and determine whether this course list
    # fulfills this requirement
    def fulfilled(self, courses: list, university: University) -> bool:
        # TODO
        # university.filterCourses(self.filter)
        # check courses in courses against filtered list
        # count uoc
        # check against self.units
        pass
