import pytest

from classes.program import Program
from classes.university import University
from classes.query_db_offline import query_db
from classes.generator import Generator
from classes.term import Term
from classes.specificCourseFilter import SpecificCourseFilter
from classes.orFilter import OrFilter
from classes.genEdFilter import GenEdFilter
from classes.freeElectiveFilter import FreeElectiveFilter

@pytest.fixture
def plan():
    '''
    Returns the default program returned by Generator
    on our current db for 3778 program
    '''
    uni = University(query_db)

    deg = uni.find_degree_number_code(3778)
    assert deg is not None

    prog = Generator(deg, uni).generate()
    assert isinstance(prog, Program)

    return prog

def test_default_outstanding_reqs(plan):
    # print current courses
    # print("")
    # print("=============== current courses ===========")
    # print(plan.courses)
    # print("===========================================")

    # list of (key, val) tuples
    reqs = list((plan.get_outstanding_reqs()).items())

    # print("============= reqs ================")
    # print(reqs)
    # print("==============================")

    assert len(reqs) == 4

    # first one is 6 UOC of COMP3900
    comp3900 = reqs[0][0]
    comp3900_uoc = reqs[0][1]
    assert comp3900_uoc == 6
    assert comp3900.uoc == 6
    assert isinstance(comp3900.filter, SpecificCourseFilter)
    assert comp3900.filter.course.course_code == "COMP3900"

    # second is 30 UOC of level 3, 4, 6, 9 COMP
    level = reqs[1][0]
    level_uoc = reqs[1][1]
    assert level_uoc == 30
    assert level.uoc == 30
    # TODO this will fail when fix AND requirements
    assert isinstance(level.filter, OrFilter)
    levels = level.filter.filters
    # TODO expand test once OR for field requirements and levels is fixed
    assert len(levels) == 4

    # third is 12 UOC of gen ed
    gens = reqs[2][0]
    gens_uoc = reqs[2][1]
    assert gens_uoc == 12
    assert gens.uoc == 12
    assert isinstance(gens.filter, GenEdFilter)

    # fourth is 36 UOC of free electives
    frees = reqs[3][0]
    frees_uoc = reqs[3][1]
    assert frees_uoc == 36
    assert frees.uoc == 36
    assert isinstance(frees.filter, FreeElectiveFilter)

    # # first one is 48 UOC of 
    # assert reqs[0][1] == 48

    # print(f"type of reqs[0] key {type(reqs[0][0])}")

    # TODO test that the field filters actually match comp level 3, 6, 9 etc.
    # right now is 
    # -----> subject requirement <DegreeReq uoc=30, filter=<OrFilter filters=[<FieldFilter field='COMP'>, <FieldFilter field='COMP'>, <FieldFilter field='COMP'>, <FieldFilter field='COMP'>]>>








def test_remove_core(plan):
    # print("=======> default plan courses")
    # print(plan.to_api())
    # print("========================")

    # have to remove CourseEnrollments
    comp1511 = plan.courses[0]
    comp1521 = plan.courses[1]
    comp1531 = plan.courses[2]
    comp2521 = plan.courses[3]

    # removing should make you not enrolled
    # and should show up as something that's needed
    plan.remove_course(comp1511)
    assert plan.enrolled(comp1511.course) == False

    # print("========== oustanding reqs ==========")
    # reqs = plan.get_outstanding_reqs()
    # print(f"length of reqs = {len(reqs)}")

    # num = 0
    # for r in reqs:
    #     if r.core_requirement:
    #         print(f"found a core: {r}")
    #         num += 1
    # print(f"printed {num} cores")
    # first_key = list(reqs.keys())[0]
    # first_val = reqs[first_key]

    # print(f"first filter type {type(first_key)}")
    # print(f"first filter value {first_val}")

    # print("=====================================")


    plan.remove_course(comp1521)
    assert plan.enrolled(comp1521.course) == False

    plan.remove_course(comp1531)
    assert plan.enrolled(comp1531.course) == False

    plan.remove_course(comp2521)
    assert plan.enrolled(comp2521.course) == False

def test_remove_elec(plan):
    # TODO add an elec and then remove it
    pass

