'''
Tests related to the API for frontend.
Generated at outermost level by calling Program.to_api()
on a Program outputted by Generator.
as in generate_program() in server/degrees.py
'''
import pytest

from classes.university import University
from classes.query_db_offline import query_db
from classes.generator import Generator
from classes.program import Program
from classes.term import Term


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


# also test via `curl http://localhost:5000/3778/gen_program.json`
def test_program_to_api():
    uni = University(query_db)

    deg = uni.find_degree_number_code(3778)
    assert deg is not None

    prog = Generator(deg, uni).generate()
    assert isinstance(prog, Program)

    api = prog.to_api()
    # print("=======> api")
    # print(api)

    assert api['id'] == 3778
    assert api['name'] == 'Computer Science'
    assert api['year'] == 2019
    assert api['duration'] == 3
    assert api['url'] == 'https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778'

    enrollments = api['enrollments']

    # visually check that enrollments are sorted
    print("=====> TODO visually check enrollments are sorted")
    print(enrollments)

def test_empty_year():
    uni = University(query_db)

    deg = uni.find_degree_number_code(3778)
    assert deg is not None

    prog = Generator(deg, uni).generate()

    # remove COMP2511,  COMP3121, COMP4920, the only things in 2021
    comp2511 = None
    comp3121 = None
    comp4920 = None
    for enr in prog.courses:
        if enr.course.course_code == "COMP2511":
            comp2511 = enr
        elif enr.course.course_code == "COMP3121":
            comp3121 = enr
        elif enr.course.course_code == "COMP4920":
            comp4920 = enr

    prog.remove_course(comp2511)
    prog.remove_course(comp3121)
    prog.remove_course(comp4920)

    # put COMP4920 in T3
    prog.add_course(comp4920.course, Term(2022, 3))

    # get the api
    api = prog.to_api()

    assert api['id'] == 3778
    assert api['name'] == 'Computer Science'
    assert api['year'] == 2019
    assert api['duration'] == 3
    assert api['url'] == 'https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778'

    enrollments = api['enrollments']

    print("=========== enrollments ===========")
    print(api)
    print(enrollments)
    print("--------------------")

    # you should still have empty information in API for T2 2021
    plan_2021 = enrollments[1]
    assert plan_2021['year'] == 2021
    assert len(plan_2021['term_plans']) == 3
    assert len(plan_2021['term_plans'][0]['course_ids']) == 0
    assert len(plan_2021['term_plans'][1]['course_ids']) == 0
    assert len(plan_2021['term_plans'][2]['course_ids']) == 0


# tests University.get_full_course
def test_get_full_course():
    uni = University(query_db)

    courses = uni.get_full_courses()
    print("====> TODO visually check a few CourseList entries")
    print(courses[:3])
    print("==========================================")
