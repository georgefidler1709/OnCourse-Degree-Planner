"""
COMP4290 Group Project
Team: On course.Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

specificCourseFilter
A filter that matches only one course

[MORE INFO ABOUT CLASS]
"""

from . import course
from . import courseFilter
from . import degree

class SpecificCourseFilter(courseFilter.CourseFilter):

    def __init__(self, course: 'course.Course'):
        super().__init__()
        self.course = course

    @property
    def info(self) -> str:
        return self.course.course_code

    # Returns whether this filters specific courses
    @property
    def core(self) -> bool:
        return True

    @property
    def field_filter(self) -> bool:
        return False

    def __repr__(self) -> str:
        return f"<SpecificCourseFilter course={self.course!r}>"

    # The name of the requirement for the database
    @property
    def filter_name(self) -> str:
        return "SpecificCourseFilter"

    # Input: course.Course, program the student is enrolled in
    # Return: Whether this course matches the filter
    def accepts_course(self, course: 'course.Course', degree: 'degree.Degree',
                eq: bool=True) -> bool:
        if course == self.course:
            return True
        elif eq and self.course.equivalent(course):
            # The entered course is equivalent to the one we want, so accept
            return True
        else:
            return False

    # Saves the filter in the database
    # Return: the id of the filter in the database
    def save(self) -> int:
        # TODO
        pass
