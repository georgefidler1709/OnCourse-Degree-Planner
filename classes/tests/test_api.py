'''
Tests related to the API for frontend.
Generated at outermost level by calling Program.to_api()
on a Program outputted by Generator.
as in generate_program() in server/degrees.py
'''
import pytest

from classes.university import University
from classes.query_db_offline import query_db


def test_CourseEnrollment_order():
	uni = University(query_db)

	comp1511 = uni.find_course("COMP1511")
	comp2521 = uni.find_course("COMP2521")
	seng1020 = uni.find_course("SENG1020")
	math1141 = uni.find_course("MATH1141")
	math1151 = uni.find_course("MATH1151")

	# less than (by extension greater than)
	# same subject, different subjects
	assert (comp1511 < comp2521) == True
	assert (comp1511 > comp2521) == False
	assert (comp2521 > comp1511) == True

	assert (comp1511 < seng1020) == True
	assert (comp1511 < math1151) == True
	assert (comp1511 > seng1020) == False
	assert (comp1511 > math1151) == False
	assert (seng1020 > comp1511) == True
	assert (math1151 > comp1511) == True

	# less than equal to (by extension greater than equal to)
	assert (comp1511 <= comp1511) == True
	assert (comp1511 <= math1141) == True
	assert (math1141 <= math1151) == True

	assert (comp1511 >= comp1511) == True
	assert (comp1511 >= math1141) == False
	assert (math1141 >= math1151) == False
	assert (math1141 >= comp1511) == True
	assert (math1141 >= comp1511) == True

	# equality
	assert (comp1511 == comp1511) == True
	assert (seng1020 == seng1020) == True

	# not equals
	assert (comp2521 != comp1511) == True
	assert (seng1020 != math1141) == True
	assert (comp1511 != comp2521) == True
	assert (math1141 != seng1020) == True

	assert (comp2521 != comp2521) == False
	assert (math1141 != math1141) == False