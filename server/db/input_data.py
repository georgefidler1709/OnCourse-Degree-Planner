'''
Insertion statements to manually populate database
'''
from .helper import Helper

def compsci_course_reqs(db="university.db"):
        '''
        Statements to insert CourseRequirements for Computer Science (3778) (COMPA1) courses
        i.e. MVP
        '''
        print("==> Inserting CourseRequirements for Computer Science 3778 (COMPA1)")
        h = Helper(dbaddr=db)

        print("Making completed course requirements...")
        # completed course reqs you can reuse
        binf4920 = h.make_course_req("completed", course="BINF4920")
        comp1911 = h.make_course_req("completed", course="COMP1911")
        comp1921 = h.make_course_req("completed", course="COMP1921")
        comp1917 = h.make_course_req("completed", course="COMP1917")
        comp1927 = h.make_course_req("completed", course="COMP1927")
        comp1927_cr = h.make_course_req("completed", course="COMP1927", min_mark=65)
        comp1511 = h.make_course_req("completed", course="COMP1511")
        comp1531 = h.make_course_req("completed", course="COMP1531")
        comp2011 = h.make_course_req("completed", course="COMP2011")
        comp2511 = h.make_course_req("completed", course="COMP2511")
        comp2521 = h.make_course_req("completed", course="COMP2521")
        comp2521_cr = h.make_course_req("completed", course="COMP2521", min_mark=65)
        comp2911 = h.make_course_req("completed", course="COMP2911")
        comp2920 = h.make_course_req("completed", course="COMP2920")
        comp3120 = h.make_course_req("completed", course="COMP3120")
        comp3121 = h.make_course_req("completed", course="COMP3121")
        comp9101 = h.make_course_req("completed", course="COMP9101")
        comp3821 = h.make_course_req("completed", course="COMP3821")
        comp9596 = h.make_course_req("completed", course="COMP9596")
        comp9801 = h.make_course_req("completed", course="COMP9801")
        comp9945 = h.make_course_req("completed", course="COMP9945")
        comp9900 = h.make_course_req("completed", course="COMP9900")
        dpst1013 = h.make_course_req("completed", course="DPST1013")
        dpst1013_cr = h.make_course_req("completed", course="DPST1013", min_mark=65)
        dpst1014 = h.make_course_req("completed", course="DPST1014")
        dpst1091 = h.make_course_req("completed", course="DPST1091")
        dpst1092 = h.make_course_req("completed", course="DPST1092")
        econ1202 = h.make_course_req("completed", course="ECON1202")
        econ2291 = h.make_course_req("completed", course="ECON2291")
        seng1020 = h.make_course_req("completed", course="SENG1020")
        seng1031 = h.make_course_req("completed", course="SENG1031")
        seng1010 = h.make_course_req("completed", course="SENG1010")
        seng4920 = h.make_course_req("completed", course="SENG4920")
        seng4921 = h.make_course_req("completed", course="SENG4921")
        math1090 = h.make_course_req("completed", course="MATH1090")
        math1011 = h.make_course_req("completed", course="MATH1011")
        math1021 = h.make_course_req("completed", course="MATH1021")
        math1031 = h.make_course_req("completed", course="MATH1031")
        math1131 = h.make_course_req("completed", course="MATH1131")
        math1131_cr = h.make_course_req("completed", course="MATH1131", min_mark=65)
        math1141 = h.make_course_req("completed", course="MATH1141")
        math1141_cr = h.make_course_req("completed", course="MATH1141", min_mark=65)
        math1151 = h.make_course_req("completed", course="MATH1151")
        math1231 = h.make_course_req("completed", course="MATH1231")
        math1241 = h.make_course_req("completed", course="MATH1241")
        math1251 = h.make_course_req("completed", course="MATH1251")

        compenrol = h.make_course_req("current", degree_id=3778)
        enrol7001 = h.make_course_req("current", degree_id=7001)
        enrol7002 = h.make_course_req("current", degree_id=7002)
        finalyear = h.make_course_req("year", year=-1)

        # COMP1511
        h.courses_exclusion_add('COMP1511', 'DPST1091')
        print("... COMP1511")

        # COMP1521
        comp1521_or = h.combine_course_req("or", [comp1511, dpst1091, comp1911, comp1917])
        h.courses_req_add("COMP1521", "pre", comp1521_or)
        h.courses_exclusion_add("COMP1521", "DPST1092")
        print("... COMP1521")

        # COMP1531
        comp1531_or = h.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
        h.courses_req_add("COMP1531", "pre", comp1531_or)
        comp1531_ex = ["SENG1020", "SENG1031", "SENG1010"]
        for exclusion in comp1531_ex:
            h.courses_exclusion_add("COMP1531", exclusion)
        print("... COMP1531")

        # COMP2511
        comp2511_small_or = h.combine_course_req("or", [comp2521, comp1927])
        comp2511_and = h.combine_course_req("and", [comp1531, comp2511_small_or])
        h.courses_req_add("COMP2511", "pre", comp2511_and)
        comp2511_ex = ["COMP2911", "COMP2011"]
        for exclusion in comp2511_ex:
            h.courses_exclusion_add("COMP2511", exclusion)
        print("... COMP2511")

        # TODO ELENI etc.

        # COMP2521
        # Prerequisite: COMP1511 or DPST1091 or COMP1917 or COMP1921
        comp2521_or = h.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
        h.courses_req_add("COMP2521", "pre", comp2521_or)
        h.courses_exclusion_add("COMP2521", "COMP1927")
        print("... COMP2521")


        # COMP3900
        # Prerequisite: COMP1531, and COMP2521 or COMP1927,
        # and enrolled in a BSc Computer Science major with completion of 102 uoc.
        comp3900_or = h.combine_course_req("or", [comp2521, comp1927])
        comp3900_uoc = h.make_course_req("uoc", uoc_amount_required=120)
        comp3900_and = h.combine_course_req("and", [comp3900_or, compenrol, comp3900_uoc])
        h.courses_req_add("COMP3900", "pre", comp3900_and)
        comp3900_ex = ["COMP9596", "COMP9945", "COMP9900"]
        for exclusion in comp3900_ex:
            h.courses_exclusion_add("COMP3900", exclusion)
        print("... COMP3900")

        # COMP4920
        # Prerequisite: COMP2511 or COMP2911, and in the final year of the BSc Computer Science
        # or BE / BE (Hons) Bioinformatics Engineering or Computer Engineering.
        # Software Engineering students enrol in SENG4920.
        comp4920_or = h.combine_course_req("or", [comp2511, comp2911])
        comp4920_and = h.combine_course_req("and", [comp4920_or, compenrol, finalyear])
        h.courses_req_add("COMP4920", "pre", comp4920_and)
        comp4920_ex = ["BINF4920", "SENG4920", "SENG4921", "COMP2920"]

        for exclusion in comp4920_ex:
            h.courses_exclusion_add("COMP4920", exclusion)
        print("... COMP4920")

        # MATH1081
        # Corequisite: MATH1131 or DPST1013 or MATH1141 or MATH1151
        math1081_or = h.combine_course_req("or", [math1131, dpst1013, math1141, math1151])
        h.courses_req_add("MATH1081", "co", math1081_or)
        h.courses_exclusion_add("MATH1081", "MATH1090")
        print("... MATH1081")

        # MATH1131
        # no prereqs
        h.courses_equivalent_add("MATH1131", "DPST1013")
        math1131_ex = ["DPST1013", "MATH1151", "MATH1031", "MATH1141", "ECON2291", "MATH1011", "ECON1202"]

        for exclusion in math1131_ex:
            h.courses_exclusion_add("MATH1131", exclusion)
        print("... MATH1131")

        # MATH1141
        math1141_ex = ["DPST1013", "MATH1151", "MATH1031", "MATH1131", "ECON2291", "MATH1011",
                "ECON1202"]

        for exclusion in math1141_ex:
            h.courses_exclusion_add("MATH1141", exclusion)
        print("... MATH1141")

        # MATH1231
        # Prerequisite: MATH1131 or DPST1013 or MATH1141
        math1231_or = h.combine_course_req("or", [math1131, dpst1013, math1141])
        h.courses_req_add("MATH1231", "pre", math1231_or)
        h.courses_equivalent_add("MATH1231", "DPST1014")
        math1231_ex = ["DPST1014", "MATH1251", "MATH1021", "MATH1241"]

        for exclusions in math1231_ex:
            h.courses_exclusion_add("MATH1231", exclusion)
        print("... MATH1231")

        # MATH1241
        # Prerequisite: MATH1131 (CR) or MATH1141 (CR) or DPST1013 (CR)
        math1241_or = h.combine_course_req("or", [math1131_cr, math1141_cr, dpst1013_cr])
        h.courses_req_add("MATH1241", "pre", math1241_or)
        math1241_ex = ["DPST1014", "MATH1251", "MATH1021", "MATH1231"]

        for exclusion in math1241_ex:
            h.courses_exclusion_add("MATH1241", exclusion)
        print("... MATH1241")

        # COMP3121
        # Prerequisite: COMP1927 or COMP2521
        comp3121_or = h.combine_course_req("or", [comp1927, comp2521])
        h.courses_req_add("COMP3121", "pre", comp3121_or)
        comp3121_eq = h.combine_course_req("and", [comp3821, comp9801, comp3120, comp9101])
        equivalent_courses = ["COMP3121", "COMP3821", "COMP9801", "COMP3120", "COMP9101"]
        for course_1 in equivalent_courses:
                for course_2 in equivalent_courses:
                        if course_1 != course_2:
                                h.courses_equivalent_add(course_1, course_2)
        print("... COMP3121")

        # COMP3821
        # Prerequisite: A mark of at least 65 in COMP1927 or COMP2521
        comp3821_or = h.combine_course_req("or", [comp1927_cr, comp2521_cr])
        h.courses_req_add("COMP3821", "pre", comp3821_or)
        comp3821_eq = h.combine_course_req("and", [comp3121, comp9801])
        print("... COMP3821")

        # DPST1013
        dpst1013_ex = ["MATH1131", "MATH1151", "MATH1031", "MATH1141", "ECON2291", "MATH1011", "ECON1202"]

        for exclusion in dpst1013_ex:
            h.courses_exclusion_add("DPST1013", exclusion)
        dpst_or = h.combine_course_req("or", [enrol7001, enrol7002])
        h.courses_req_add("DPST1013", "pre", dpst_or)
        print("... DPST1013")

        # DPST1014
        dpst1014_ex = ["MATH1231", "MATH1241", "MATH1251", "MATH1021"]

        for exclusion in dpst1014_ex:
            h.courses_exclusion_add("DPST1014", exclusion)
        h.courses_req_add("DPST1014", "pre", dpst_or)
        print("... DPST1014")

        h.close()

def insert_sessions(start=2019, end=2025, db='university.db'):
        '''
        Populates all terms (0-3) for given range of years
        '''
        print(f"==> Inserting Sessions from {start} to {end}")
        h = Helper(dbaddr=db)

        h.add_sessions(start, end)

        h.close()

def insert_course_offerings(start=2019, end=2025, db='university.db'):
        '''
        inserts course offerings for computer science 3778 COMPA1 related courses
        <start> <end> specify range of years to insert course offerings for
        if term offerings are assumed to be the same for those years
        '''
        print(f"==> Inserting Course Offerings for COMPA1 Degree")

        years = list(range(start, end + 1))

        h = Helper(dbaddr=db)

        all_terms_courses = ["DPST1091", "COMP1511", "DPST1092", "COMP3900", 
                "COMP9900", "MATH1081", "MATH1131", "DPST1013", "MATH1231",
                "DPST1014"]

        t1_courses = ["COMP1531", "COMP2521", "MATH1141", "MATH1241", "MATH1031",
                "MATH1011", "ECON1202", "COMP3821", "COMP9801"]

        t2_courses = ["COMP1521", "COMP1911", "COMP2511", "MATH1241", "COMP3121",
                "COMP9101", "MATH1251"]

        t3_courses = ["COMP1521", "COMP1531", "COMP2511", "COMP2521", "COMP4920",
                "SENG4920", "MATH1141", "MATH1031", "MATH1011", "ECON1202"]

        summer_courses = ["ECON1202"]

        print("... courses in t1, t2, t3")
        for course in all_terms_courses:
                h.add_course_offerings(course, years, [1, 2, 3])

        print("... courses in t1")
        for course in t1_courses:
                h.add_course_offerings(course, years, [1])

        print("... courses in t2")
        for course in t2_courses:
                h.add_course_offerings(course, years, [2])

        print("... courses in t3")
        for course in t3_courses:
                h.add_course_offerings(course, years, [3])

        print("... summer courses")
        for course in summer_courses:
                h.add_course_offerings(course, years, [0])

        h.close()

def insert_compsci_degree_requirements(db='university.db', start_year=2020, end_year=2023):
        '''
        Inserts CourseFilters for COMPA1 degree and combines them into 
        DegreeOfferingRequirements
        '''
        print("==> Inserting Course Filters for COMPA1 Degree")

        h = Helper(dbaddr=db)

        # specific course filters
        core_courses = ["COMP1511", "COMP1521", "COMP1531", "COMP2511",
                "COMP2521", "COMP3900", "COMP4920", "MATH1081"]
        math1_opts = ["MATH1131", "MATH1141"]
        math2_opts = ["MATH1231", "MATH1241"]
        algos_opts = ["COMP3121", "COMP3821"]

        print("... core courses filters")
        core_filters = h.spec_courses_to_filters(core_courses)

        # core_combo = h.combine_course_filters("or", core_filters)

        math1_filters = h.spec_courses_to_filters(math1_opts)
        math1_or = h.combine_course_filters("or", math1_filters)

        math2_filters = h.spec_courses_to_filters(math2_opts)
        math2_or = h.combine_course_filters("or", math2_filters)

        algos_filters = h.spec_courses_to_filters(algos_opts)
        algos_or = h.combine_course_filters("or", algos_filters)

        # comp elective filters, 30 UOC level 3, 4, 6, 9
        # "I guess you'd have OR(AND(COMP, level 3), AND(COMP, level4)) etc" - Eleni
        # WARNING making levels a part of filter that can be None / NULL if you just need any COMP course
        level3 = h.add_course_filter("level", level=3)
        level4 = h.add_course_filter("level", level=4)
        level6 = h.add_course_filter("level", level=6)
        level9 = h.add_course_filter("level", level=9)

        comp = h.add_course_filter("field", field_code="COMP")
        level3_or_above = h.combine_course_filters("or", [level3, level4, level6, level9])

        comp_elec = h.combine_course_filters("and", [comp, level3_or_above])

        # gen ed filters, 12 UOC
        gen_filter = h.add_course_filter("gen")

        # free elective filters, 36 UOC
        free_filter = h.add_course_filter("free")

        # ====== insert degree requirements =====
        print("===> Inserting Degree Requirements for COMPA1 Degree")
        COURSE_UOC = 6
        COMPSCI = 3778

        print("Inserting degree...")
        h.add_degree("Computer Science", "Engineering", 3, COMPSCI)

        print("Inserting degree offerings and requirements...")
        for year in range(start_year, end_year + 1):
                h.add_degree_offering(year, COMPSCI)
                print(f"... year {year}")

                # TODO would have to insert these in a loop to get all the degree offerings inserted
                for f in core_filters:
                        h.add_degree_reqs(COMPSCI, year, f, COURSE_UOC)
                # h.add_degree_reqs(COMPSCI, 2019, core_combo, len(core_courses) * COURSE_UOC)
                h.add_degree_reqs(COMPSCI, year, math1_or, COURSE_UOC)
                h.add_degree_reqs(COMPSCI, year, math2_or, COURSE_UOC)
                h.add_degree_reqs(COMPSCI, year, algos_or, COURSE_UOC)

                # 30 UOC comp electives
                h.add_degree_reqs(COMPSCI, year, comp_elec, 30)
                
                # 12 UOC gen eds
                h.add_degree_reqs(COMPSCI, year, gen_filter, 12)

                # 36 UOC free electives
                h.add_degree_reqs(COMPSCI, year, free_filter, 36)

                # total UOC = 144
                h.add_degree_reqs(COMPSCI, year, None, 144)

        h.close()

def insert_seng_degree_requirements(db='university.db', start_year=2020, end_year=2023):
        # WARNING current degree structure means this is the only "Engineering Hons" degree that can be represented

        # https://www.handbook.unsw.edu.au/undergraduate/programs/2020/3707
        # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/SENGAH

        print("==> Inserting Course Filters for SENGAH Degree")

        # level 1 core courses
        core_l1 = ["COMP1511", "COMP1521", "COMP1531", "ENGG100", "MATH1081"]
        math1_opts = ["MATH1131", "MATH1141"]
        math2_opts = ["MATH1231", "MATH1241"]

        # level 2 core courses
        core_l2 = ["COMP2041", "COMP2511", "COMP2521", "DESN2000", "SENG2011", "SENG2021"]
        l2_3UOC = ["MATH2400", "MATH2859"]

        # level 3 core courses 
        core_l3 = ["COMP3141", "COMP3311", "COMP3331", "SENG3011"]

        # level 4 core course
        core_l4 = ["COMP4920"]
        hons = ["COMP4951", "COMP4952", "COMP4953"] # 4 UOC each

        # insert the specific course filters
        core_l1_filters = h.spec_courses_to_filters(core_l1)

        math1_filters = h.spec_courses_to_filters(math1_opts)
        math1_or = h.combine_course_filters("or", math1_filters)

        math2_filters = h.spec_courses_to_filters(math2_opts)
        math2_or = h.combine_course_filters("or", math2_filters)

        core_l2_filters = h.spec_courses_to_filters(core_l2)
        l2_3UOC_filters = h.spec_courses_to_filters(l2_3UOC)

        core_l3_filters = h.spec_courses_to_filters(core_l3)

        core_l4_filters = h.spec_courses_to_filters(core_l4)
        hons_filters = h.spec_courses_to_filters(hons)

        # TODO insert the discipline electives filters, 36 UOC
        # make sure this is the same as the one for general SENG
        level3 = h.add_course_filter("level", level=3)
        level4 = h.add_course_filter("level", level=4)
        level6 = h.add_course_filter("level", level=6)
        level9 = h.add_course_filter("level", level=9)

        # any level 3, 4, 6, 9 computer science
        comp = h.add_course_filter("field", field_code="COMP")
        comp_levels = h.combine_course_filters("or", [level3, level4, level6, level9])
        comp_disc = h.combine_course_filters("and", [comp, comp_levels])

        # any level 3, 4 electrical engineering
        elec = h.add_course_filter("field", field_code="ELEC")
        elec_levels = h.combine_course_filters("or", [level3, level4])
        elec_disc = h.combine_course_filters("and", [elec, elec_levels])

        # ENGG3060, 3 UOC
        maker = h.add_course_filter("spec", min_mark=50, course="ENGG3060")

        # any level 3, 4 infosys
        infs = h.add_course_filter("field", field_code="INFS")
        infs_levels = h.combine_course_filters("or", [level3, level4])
        infs_disc = h.combine_course_filters("and", [infs, infs_levels])

        # any level 3, 4, 6 MATH
        math = h.add_course_filter("field", field_code="MATH")
        math_levels = h.combine_course_filters("or", [level3, level4, level6])
        math_disc = h.combine_course_filters("and", [math, math_levels])

        # any level 3, 4 TELE
        tele = h.add_course_filter("field", field_code = "TELE")
        tele_levels = h.combine_course_filters("or", [level3, level4])
        tele_disc = h.combine_course_filters("and", [tele, tele_levels])

        # discipline elective filter
        disc_filter = h.combine_course_filters("or", [comp_disc, elec_disc, maker, infs_disc, math_disc, tele_disc])

        gen_filter = h.add_course_filter("gen")
        free_filter = h.add_course_filter("free")

        print("==> Inserting Degree Requirements for SENGAH Degree")

        SENG = 3707

        print("Inserting degree...")
        h.add_degree("Engineering (Honours) (Software Engineering)", "Engineering", 4, SENG)

        print("Inserting degree offerings and requirements...")
        for year in range(start_year, end_year + 1):
                print(f"... year {year}")
                h.add_degree_offering(year, SENG)

                # 168 UOC stream: SENGAH

                # 6 UOC specific courses
                uoc_6 = core_l1_filters + math1_or + math2_or + core_l2_filters + core_l3_filters + core_l4_filters
                for f in uoc_6:
                        h.add_degree_reqs(SENG, year, f, 6)

                # 3 UOC specific courses
                uoc_3 = l2_3UOC_filters
                for f in uoc_3:
                        h.add_degree_reqs(SENG, year, f, 3)

                # 4 UOC specific courses
                uoc_4 = hons_filters
                for f in uoc_4:
                        h.add_degree_reqs(SENG, year, f, 4)

                # 36 UOC discipline electives
                h.add_degree_reqs(SENG, year, disc_filter, 36)

                # 6 UOC free electives
                h.add_degree_reqs(SENG, year, free_filter, 6)

                # level requirements, maturity requirements
                # 30 UOC level 4 or higher COMP
                h.add_degree_notes(SENG, year, "Students must complete a minimum of 30 UOC of the following courses: any level 4, 6, 9 Computer Science course, COMP4920, COMP4951, COMP4952, COMP4953.")

                # level 3 maturity requirements
                # students must coimplete 42 UOC before taking any level 3 course
                h.add_degree_notes(SENG, year, "Students must have completed 42 UOC before taking any level 3 course.")

                # level 4 maturity requirements
                # students must complete 102 UOC before taking any level 4 course
                h.add_degree_notes(SENG, year, "Students must have completed 102 UOC before taking any level 4 course.")

                # 12 UOC General Education
                h.add_degree_reqs(SENG, year, gen_filter, 12)

                # 12 UOC Discipline Electives
                h.add_degree_reqs(SENG, year, disc_filter, 12)

                # 60 days of Industrial Training?
                h.add_degree_notes(SENG, year, "Students must have completed a minimum of 60 days of Industrial Training to graduate. Industrial training must be undrtaken concurrently with enrolment in the program.")

                # total UOC = 192
                h.add_degree_reqs(SENG, year, None, 192)


if __name__ == "__main__":
        
        # Computer Science (3778) (COMPA1) courses
        # compsci_course_reqs()
        # insert_sessions()
        # insert_course_offerings()
        # insert_compsci_degree_requirements()
        insert_seng_degree_requirements()

        pass
