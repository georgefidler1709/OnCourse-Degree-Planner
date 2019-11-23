'''
Insertion statements to manually populate database
'''
from .helper import Helper

def compsci_course_reqs(db='university.db'):
        '''
        Statements to insert CourseRequirements for Computer Science (3778) (COMPA1) courses
        i.e. MVP
        '''
        print('==> Inserting CourseRequirements for Computer Science 3778 (COMPA1)')
        h = Helper(dbaddr=db)

        print('Making completed course requirements...')
        # completed course reqs you can reuse
        binf4920 = h.make_course_req('completed', course='BINF4920')
        comp1911 = h.make_course_req('completed', course='COMP1911')
        comp1921 = h.make_course_req('completed', course='COMP1921')
        comp1917 = h.make_course_req('completed', course='COMP1917')
        comp1927 = h.make_course_req('completed', course='COMP1927')
        comp1927_cr = h.make_course_req('completed', course='COMP1927', min_mark=65)
        comp1511 = h.make_course_req('completed', course='COMP1511')
        comp1531 = h.make_course_req('completed', course='COMP1531')
        comp2011 = h.make_course_req('completed', course='COMP2011')
        comp2511 = h.make_course_req('completed', course='COMP2511')
        comp2521 = h.make_course_req('completed', course='COMP2521')
        comp2521_cr = h.make_course_req('completed', course='COMP2521', min_mark=65)
        comp2911 = h.make_course_req('completed', course='COMP2911')
        comp2920 = h.make_course_req('completed', course='COMP2920')
        comp3120 = h.make_course_req('completed', course='COMP3120')
        comp3121 = h.make_course_req('completed', course='COMP3121')
        comp9101 = h.make_course_req('completed', course='COMP9101')
        comp3821 = h.make_course_req('completed', course='COMP3821')
        comp9596 = h.make_course_req('completed', course='COMP9596')
        comp9801 = h.make_course_req('completed', course='COMP9801')
        comp9945 = h.make_course_req('completed', course='COMP9945')
        comp9900 = h.make_course_req('completed', course='COMP9900')
        dpst1013 = h.make_course_req('completed', course='DPST1013')
        dpst1013_cr = h.make_course_req('completed', course='DPST1013', min_mark=65)
        dpst1014 = h.make_course_req('completed', course='DPST1014')
        dpst1091 = h.make_course_req('completed', course='DPST1091')
        dpst1092 = h.make_course_req('completed', course='DPST1092')
        econ1202 = h.make_course_req('completed', course='ECON1202')
        econ2291 = h.make_course_req('completed', course='ECON2291')
        seng1020 = h.make_course_req('completed', course='SENG1020')
        seng1031 = h.make_course_req('completed', course='SENG1031')
        seng1010 = h.make_course_req('completed', course='SENG1010')
        seng4920 = h.make_course_req('completed', course='SENG4920')
        seng4921 = h.make_course_req('completed', course='SENG4921')
        math1090 = h.make_course_req('completed', course='MATH1090')
        math1011 = h.make_course_req('completed', course='MATH1011')
        math1021 = h.make_course_req('completed', course='MATH1021')
        math1031 = h.make_course_req('completed', course='MATH1031')
        math1131 = h.make_course_req('completed', course='MATH1131')
        math1131_cr = h.make_course_req('completed', course='MATH1131', min_mark=65)
        math1141 = h.make_course_req('completed', course='MATH1141')
        math1141_cr = h.make_course_req('completed', course='MATH1141', min_mark=65)
        math1151 = h.make_course_req('completed', course='MATH1151')
        math1231 = h.make_course_req('completed', course='MATH1231')
        math1241 = h.make_course_req('completed', course='MATH1241')
        math1251 = h.make_course_req('completed', course='MATH1251')

        compenrol = h.make_course_req('current', degree_id=3778)
        enrol7001 = h.make_course_req('current', degree_id=7001)
        enrol7002 = h.make_course_req('current', degree_id=7002)
        finalyear = h.make_course_req('year', year=-1)

        # COMP1511
        h.courses_exclusion_add('COMP1511', 'DPST1091')
        print('... COMP1511')

        # COMP1521
        comp1521_or = h.combine_course_req('or', [comp1511, dpst1091, comp1911, comp1917])
        h.courses_req_add('COMP1521', 'pre', comp1521_or)
        h.courses_exclusion_add('COMP1521', 'DPST1092')
        print('... COMP1521')

        # COMP1531
        comp1531_or = h.combine_course_req('or', [comp1511, dpst1091, comp1917, comp1921])
        h.courses_req_add('COMP1531', 'pre', comp1531_or)
        comp1531_ex = ['SENG1020', 'SENG1031', 'SENG1010']
        for exclusion in comp1531_ex:
            h.courses_exclusion_add('COMP1531', exclusion)
        print('... COMP1531')

        # COMP2511
        comp2511_small_or = h.combine_course_req('or', [comp2521, comp1927])
        comp2511_and = h.combine_course_req('and', [comp1531, comp2511_small_or])
        h.courses_req_add('COMP2511', 'pre', comp2511_and)
        comp2511_ex = ['COMP2911', 'COMP2011']
        for exclusion in comp2511_ex:
            h.courses_exclusion_add('COMP2511', exclusion)
        print('... COMP2511')

        # TODO ELENI etc.

        # COMP2521
        # Prerequisite: COMP1511 or DPST1091 or COMP1917 or COMP1921
        comp2521_or = h.combine_course_req('or', [comp1511, dpst1091, comp1917, comp1921])
        h.courses_req_add('COMP2521', 'pre', comp2521_or)
        h.courses_exclusion_add('COMP2521', 'COMP1927')
        print('... COMP2521')


        # COMP3900
        # Prerequisite: COMP1531, and COMP2521 or COMP1927,
        # and enrolled in a BSc Computer Science major with completion of 102 uoc.
        comp3900_or = h.combine_course_req('or', [comp2521, comp1927])
        comp3900_uoc = h.make_course_req('uoc', uoc_amount_required=120)
        comp3900_and = h.combine_course_req('and', [comp3900_or, compenrol, comp3900_uoc])
        h.courses_req_add('COMP3900', 'pre', comp3900_and)
        comp3900_ex = ['COMP9596', 'COMP9945', 'COMP9900']
        for exclusion in comp3900_ex:
            h.courses_exclusion_add('COMP3900', exclusion)
        print('... COMP3900')

        # COMP4920
        # Prerequisite: COMP2511 or COMP2911, and in the final year of the BSc Computer Science
        # or BE / BE (Hons) Bioinformatics Engineering or Computer Engineering.
        # Software Engineering students enrol in SENG4920.
        comp4920_or = h.combine_course_req('or', [comp2511, comp2911])
        comp4920_and = h.combine_course_req('and', [comp4920_or, compenrol, finalyear])
        h.courses_req_add('COMP4920', 'pre', comp4920_and)
        comp4920_ex = ['BINF4920', 'SENG4920', 'SENG4921', 'COMP2920']

        for exclusion in comp4920_ex:
            h.courses_exclusion_add('COMP4920', exclusion)
        print('... COMP4920')

        # MATH1081
        # Corequisite: MATH1131 or DPST1013 or MATH1141 or MATH1151
        math1081_or = h.combine_course_req('or', [math1131, dpst1013, math1141, math1151])
        h.courses_req_add('MATH1081', 'co', math1081_or)
        h.courses_exclusion_add('MATH1081', 'MATH1090')
        print('... MATH1081')

        # MATH1131
        # no prereqs
        h.courses_equivalent_add('MATH1131', 'DPST1013')
        math1131_ex = ['DPST1013', 'MATH1151', 'MATH1031', 'MATH1141', 'ECON2291', 'MATH1011', 'ECON1202']

        for exclusion in math1131_ex:
            h.courses_exclusion_add('MATH1131', exclusion)
        print('... MATH1131')

        # MATH1141
        math1141_ex = ['DPST1013', 'MATH1151', 'MATH1031', 'MATH1131', 'ECON2291', 'MATH1011',
                'ECON1202']

        for exclusion in math1141_ex:
            h.courses_exclusion_add('MATH1141', exclusion)
        print('... MATH1141')

        # MATH1231
        # Prerequisite: MATH1131 or DPST1013 or MATH1141
        math1231_or = h.combine_course_req('or', [math1131, dpst1013, math1141])
        h.courses_req_add('MATH1231', 'pre', math1231_or)
        h.courses_equivalent_add('MATH1231', 'DPST1014')
        math1231_ex = ['DPST1014', 'MATH1251', 'MATH1021', 'MATH1241']

        for exclusions in math1231_ex:
            h.courses_exclusion_add('MATH1231', exclusion)
        print('... MATH1231')

        # MATH1241
        # Prerequisite: MATH1131 (CR) or MATH1141 (CR) or DPST1013 (CR)
        math1241_or = h.combine_course_req('or', [math1131_cr, math1141_cr, dpst1013_cr])
        h.courses_req_add('MATH1241', 'pre', math1241_or)
        math1241_ex = ['DPST1014', 'MATH1251', 'MATH1021', 'MATH1231']

        for exclusion in math1241_ex:
            h.courses_exclusion_add('MATH1241', exclusion)
        print('... MATH1241')

        # COMP3121
        # Prerequisite: COMP1927 or COMP2521
        comp3121_or = h.combine_course_req('or', [comp1927, comp2521])
        h.courses_req_add('COMP3121', 'pre', comp3121_or)
        comp3121_eq = h.combine_course_req('and', [comp3821, comp9801, comp3120, comp9101])
        equivalent_courses = ['COMP3121', 'COMP3821', 'COMP9801', 'COMP3120', 'COMP9101']
        for course_1 in equivalent_courses:
                for course_2 in equivalent_courses:
                        if course_1 != course_2:
                                h.courses_equivalent_add(course_1, course_2)
        print('... COMP3121')

        # COMP3821
        # Prerequisite: A mark of at least 65 in COMP1927 or COMP2521
        comp3821_or = h.combine_course_req('or', [comp1927_cr, comp2521_cr])
        h.courses_req_add('COMP3821', 'pre', comp3821_or)
        comp3821_eq = h.combine_course_req('and', [comp3121, comp9801])
        print('... COMP3821')

        # DPST1013
        dpst1013_ex = ['MATH1131', 'MATH1151', 'MATH1031', 'MATH1141', 'ECON2291', 'MATH1011', 'ECON1202']

        for exclusion in dpst1013_ex:
            h.courses_exclusion_add('DPST1013', exclusion)
        dpst_or = h.combine_course_req('or', [enrol7001, enrol7002])
        h.courses_req_add('DPST1013', 'pre', dpst_or)
        print('... DPST1013')

        # DPST1014
        dpst1014_ex = ['MATH1231', 'MATH1241', 'MATH1251', 'MATH1021']

        for exclusion in dpst1014_ex:
            h.courses_exclusion_add('DPST1014', exclusion)
        h.courses_req_add('DPST1014', 'pre', dpst_or)
        print('... DPST1014')

        h.close()

def insert_sessions(start=2019, end=2025, db='university.db'):
        '''
        Populates all terms (0-3) for given range of years
        '''
        print(f'==> Inserting Sessions from {start} to {end}')
        h = Helper(dbaddr=db)

        h.add_sessions(start, end)

        h.close()

def insert_course_offerings(start=2019, end=2025, db='university.db'):
        '''
        inserts course offerings for computer science 3778 COMPA1 related courses
        <start> <end> specify range of years to insert course offerings for
        if term offerings are assumed to be the same for those years
        '''
        print(f'==> Inserting Course Offerings for COMPA1 Degree')

        years = list(range(start, end + 1))

        h = Helper(dbaddr=db)

        all_terms_courses = ['DPST1091', 'COMP1511', 'DPST1092', 'COMP3900', 
                'COMP9900', 'MATH1081', 'MATH1131', 'DPST1013', 'MATH1231',
                'DPST1014']

        t1_courses = ['COMP1531', 'COMP2521', 'MATH1141', 'MATH1241', 'MATH1031',
                'MATH1011', 'ECON1202', 'COMP3821', 'COMP9801']

        t2_courses = ['COMP1521', 'COMP1911', 'COMP2511', 'MATH1241', 'COMP3121',
                'COMP9101', 'MATH1251']

        t3_courses = ['COMP1521', 'COMP1531', 'COMP2511', 'COMP2521', 'COMP4920',
                'SENG4920', 'MATH1141', 'MATH1031', 'MATH1011', 'ECON1202']

        summer_courses = ['ECON1202']

        print('... courses in t1, t2, t3')
        for course in all_terms_courses:
                h.add_course_offerings(course, years, [1, 2, 3])

        print('... courses in t1')
        for course in t1_courses:
                h.add_course_offerings(course, years, [1])

        print('... courses in t2')
        for course in t2_courses:
                h.add_course_offerings(course, years, [2])

        print('... courses in t3')
        for course in t3_courses:
                h.add_course_offerings(course, years, [3])

        print('... summer courses')
        for course in summer_courses:
                h.add_course_offerings(course, years, [0])

        h.close()

def insert_compsci_degree_requirements(db='university.db', start_year=2020, end_year=2021):
        '''
        Inserts CourseFilters for COMPA1 degree and combines them into 
        DegreeOfferingRequirements
        '''
        print('==> Inserting Course Filters for COMPA1 Degree')

        h = Helper(dbaddr=db)

        # specific course filters
        core_courses = ['COMP1511', 'COMP1521', 'COMP1531', 'COMP2511',
                'COMP2521', 'COMP3900', 'COMP4920', 'MATH1081']
        math1_opts = ['MATH1131', 'MATH1141']
        math2_opts = ['MATH1231', 'MATH1241']
        algos_opts = ['COMP3121', 'COMP3821']

        print('... core courses filters')
        core_filters = h.spec_courses_to_filters(core_courses)

        # core_combo = h.combine_course_filters('or', core_filters)

        math1_filters = h.spec_courses_to_filters(math1_opts)
        math1_or = h.combine_course_filters('or', math1_filters)

        math2_filters = h.spec_courses_to_filters(math2_opts)
        math2_or = h.combine_course_filters('or', math2_filters)

        algos_filters = h.spec_courses_to_filters(algos_opts)
        algos_or = h.combine_course_filters('or', algos_filters)

        # comp elective filters, 30 UOC level 3, 4, 6, 9
        # 'I guess you'd have OR(AND(COMP, level 3), AND(COMP, level4)) etc' - Eleni
        # WARNING making levels a part of filter that can be None / NULL if you just need any COMP course
        level3 = h.add_course_filter('level', level=3)
        level4 = h.add_course_filter('level', level=4)
        level6 = h.add_course_filter('level', level=6)
        level9 = h.add_course_filter('level', level=9)

        comp = h.add_course_filter('field', field_code='COMP')
        level3_or_above = h.combine_course_filters('or', [level3, level4, level6, level9])

        comp_elec = h.combine_course_filters('and', [comp, level3_or_above])

        # gen ed filters, 12 UOC
        gen_filter = h.add_course_filter('gen')

        # free elective filters, 36 UOC
        free_filter = h.add_course_filter('free')

        # ====== insert degree requirements =====
        print('===> Inserting Degree Requirements for COMPA1 Degree')
        COURSE_UOC = 6
        COMPSCI = '3778 COMPA1'

        print('Inserting degree...')
        h.add_degree('Computer Science', 'Faculty of Engineering', 3, COMPSCI)

        print('Inserting degree offerings and requirements...')
        for year in range(start_year, end_year + 1):
                h.add_degree_offering(year, COMPSCI)
                print(f'... year {year}')

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

def insert_seng_degree_requirements(db='university.db', start_year=2020, end_year=2021):
        # https://www.handbook.unsw.edu.au/undergraduate/programs/2020/3707
        # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/SENGAH

        print('==> Inserting Course Filters for SENGAH Degree')
        h = Helper(dbaddr=db)

        # level 1 core courses
        core_l1 = ['COMP1511', 'COMP1521', 'COMP1531', 'ENGG1000', 'MATH1081']
        math1_opts = ['MATH1131', 'MATH1141']
        math2_opts = ['MATH1231', 'MATH1241']

        # level 2 core courses
        core_l2 = ['COMP2041', 'COMP2511', 'COMP2521', 'DESN2000', 'SENG2011', 'SENG2021']
        l2_3UOC = ['MATH2400', 'MATH2859']

        # level 3 core courses 
        core_l3 = ['COMP3141', 'COMP3311', 'COMP3331', 'SENG3011']

        # level 4 core course
        core_l4 = ['SENG4920']
        hons = ['COMP4951', 'COMP4952', 'COMP4953'] # 4 UOC each

        # insert the specific course filters
        core_l1_filters = h.spec_courses_to_filters(core_l1)

        math1_filters = h.spec_courses_to_filters(math1_opts)
        math1_or = h.combine_course_filters('or', math1_filters)

        math2_filters = h.spec_courses_to_filters(math2_opts)
        math2_or = h.combine_course_filters('or', math2_filters)

        core_l2_filters = h.spec_courses_to_filters(core_l2)
        l2_3UOC_filters = h.spec_courses_to_filters(l2_3UOC)

        core_l3_filters = h.spec_courses_to_filters(core_l3)

        core_l4_filters = h.spec_courses_to_filters(core_l4)
        hons_filters = h.spec_courses_to_filters(hons)

        # TODO insert the discipline electives filters, 36 UOC
        # make sure this is the same as the one for general SENG
        level3 = h.add_course_filter('level', level=3)
        level4 = h.add_course_filter('level', level=4)
        level6 = h.add_course_filter('level', level=6)
        level9 = h.add_course_filter('level', level=9)

        # any level 3, 4, 6, 9 computer science
        comp = h.add_course_filter('field', field_code='COMP')
        comp_levels = h.combine_course_filters('or', [level3, level4, level6, level9])
        comp_disc = h.combine_course_filters('and', [comp, comp_levels])

        # any level 3, 4 electrical engineering
        elec = h.add_course_filter('field', field_code='ELEC')
        elec_levels = h.combine_course_filters('or', [level3, level4])
        elec_disc = h.combine_course_filters('and', [elec, elec_levels])

        # ENGG3060, 3 UOC
        maker = h.add_course_filter('spec', min_mark=50, course='ENGG3060')

        # any level 3, 4 infosys
        infs = h.add_course_filter('field', field_code='INFS')
        infs_levels = h.combine_course_filters('or', [level3, level4])
        infs_disc = h.combine_course_filters('and', [infs, infs_levels])

        # any level 3, 4, 6 MATH
        math = h.add_course_filter('field', field_code='MATH')
        math_levels = h.combine_course_filters('or', [level3, level4, level6])
        math_disc = h.combine_course_filters('and', [math, math_levels])

        # any level 3, 4 TELE
        tele = h.add_course_filter('field', field_code = 'TELE')
        tele_levels = h.combine_course_filters('or', [level3, level4])
        tele_disc = h.combine_course_filters('and', [tele, tele_levels])

        # discipline elective filter
        disc_filter = h.combine_course_filters('or', [comp_disc, elec_disc, maker, infs_disc, math_disc, tele_disc])

        gen_filter = h.add_course_filter('gen')
        free_filter = h.add_course_filter('free')

        print('==> Inserting Degree Requirements for SENGAH Degree')

        SENG = '3707 SENGAH'

        print('Inserting degree...')
        h.add_degree('Engineering (Honours) (Software Engineering)', 'Faculty of Engineering', 4, SENG)

        print('Inserting degree offerings and requirements...')
        for year in range(start_year, end_year + 1):
                print(f'... year {year}')
                h.add_degree_offering(year, SENG)

                # 168 UOC stream: SENGAH

                # 6 UOC specific courses
                uoc_6 = core_l1_filters + [math1_or] + [math2_or] + core_l2_filters + core_l3_filters + core_l4_filters
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

                # 36 UOC discipline electives + 12 UOC discipline electives for ENGG degree
                h.add_degree_reqs(SENG, year, disc_filter, 36 + 12, 'Discipline Electives')

                # 12 UOC Discipline Electives
                # h.add_degree_reqs(SENG, year, disc_filter, 12, 'Discipline Electives')

                # 6 UOC free electives
                h.add_degree_reqs(SENG, year, free_filter, 6)

                # discipline electives notes
                h.add_degree_notes(SENG, year, 'Discipline Electives include: any level 3, 4, 6, 9 COMP course; any level 3, 4 ELEC Course; ENGG3060; any level 3, 4, INFS course; any level 3, 4, 6 MATH course; any level 3, 4, TELE course')

                # level requirements, maturity requirements
                # 30 UOC level 4 or higher COMP
                h.add_degree_notes(SENG, year, 'Students must complete a minimum of 30 UOC of the following courses: any level 4, 6, 9 Computer Science course, COMP4920, COMP4951, COMP4952, COMP4953.')

                # level 3 maturity requirements
                # students must coimplete 42 UOC before taking any level 3 course
                h.add_degree_notes(SENG, year, 'Students must have completed 42 UOC before taking any level 3 course.')

                # level 4 maturity requirements
                # students must complete 102 UOC before taking any level 4 course
                h.add_degree_notes(SENG, year, 'Students must have completed 102 UOC before taking any level 4 course.')

                # 12 UOC General Education
                h.add_degree_reqs(SENG, year, gen_filter, 12)
                

                # 60 days of Industrial Training?
                h.add_degree_notes(SENG, year, 'Students must have completed a minimum of 60 days of Industrial Training to graduate. Industrial training must be undertaken concurrently with enrolment in the program.')

                # total UOC = 192
                h.add_degree_reqs(SENG, year, None, 192)


def insert_degrees_with_no_offerings(db='university.db'):
    # these degrees are used in course requirements but we don't have the full requirements for them
    print('==> Degrees with no offerings')
    h = Helper(dbaddr=db)

    h.add_degree('Science', 'Faculty of Science', 1, 7001)
    h.add_degree('Engineering', 'Faculty of Engineering', 1, 7002)

def insert_binf_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/BINFAH
    h = Helper(dbaddr=db)

    # ===> start filters needed

    # level 1 spec
    core_l1_filters = h.spec_courses_to_filters(['BABS1201', 'COMP1511', 'COMP1521', 'COMP1531',
        'ENGG1000', 'MATH1081'])
    
    chem_filters = h.spec_courses_to_filters(['CHEM1011', 'CHEM1031'])
    chem_or = h.combine_course_filters('or', chem_filters)

    phys_filters = h.spec_courses_to_filters(['PHYS1111', 'PHYS1121', 'PHYS1131'])
    phys_or = h.combine_course_filters('or', phys_filters)

    math1_filters = h.spec_courses_to_filters(['MATH1131', 'MATH1141'])    
    math1_or = h.combine_course_filters('or', math1_filters)

    math2_filters = h.spec_courses_to_filters(['MATH1231', 'MATH1241'])
    math2_or = h.combine_course_filters('or', math2_filters)

    # level 2 spec
    core_l2_filters = h.spec_courses_to_filters(['BINF2010', 'BIOC2201', 'COMP2041', 'COMP2511',
        'COMP2521', 'DESN2000'])

    mathl2_filters = h.spec_courses_to_filters(['MATH2801', 'MATH2901'])
    mathl2_or = h.combine_course_filters('or', mathl2_filters)

    sci2_filters = h.spec_courses_to_filters(['BABS2202', 'BABS2204', 'BABS2264', 'BIOC2101', 'MICR2011'])
    sci2_or = h.combine_course_filters('or', sci2_filters)

    # level 3 spec
    core_l3_filters = h.spec_courses_to_filters(['BABS3121', 'BINF3010', 'COMP3121', 'COMP3311'])

    # level 4 spec
    core_l4_filters = h.spec_courses_to_filters(['BINF6112', 'COMP4920'])

    # 4 uoc ones
    hons_filters = h.spec_courses_to_filters(['COMP4951', 'COMP4952', 'COMP4953'])

    # general education
    gen_filter = h.add_course_filter('gen')

    # discipline electives
    level3 = h.add_course_filter('level', level=3)
    level4 = h.add_course_filter('level', level=4)
    level6 = h.add_course_filter('level', level=6)
    level9 = h.add_course_filter('level', level=9)

    # any level 3, 4, 6, 9 computer science
    comp = h.add_course_filter('field', field_code='COMP')
    comp_levels = h.combine_course_filters('or', [level3, level4, level6, level9])
    comp_disc = h.combine_course_filters('and', [comp, comp_levels])

    # any level 3 BABS
    babs = h.add_course_filter('field', field_code='BABS')
    babs_disc = h.combine_course_filters('and', [babs, level3])

    # any level 3 BIOC
    bioc = h.add_course_filter('field', field_code='BIOC')
    bioc_disc = h.combine_course_filters('and', [bioc, level3])

    # any level 3 MICR
    micr = h.add_course_filter('field', field_code='MICR')
    micr_disc = h.combine_course_filters('and', [micr, level3])

    # ENGG3060
    maker = h.add_course_filter('spec', min_mark=50, course='ENGG3060')

    disc_filter = h.combine_course_filters('or', [comp_disc, babs_disc, bioc_disc, micr_disc, maker])


    # ===> end filters needed


    print('==> Inserting Degree Requirements for BINFAH Degree')

    BINF = '3707 BINFAH'

    print('Inserting degree...')
    h.add_degree('Engineering (Honours) (Bioinformatics)', 'Faculty of Engineering', 4, BINF)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, BINF)

        # 168 UOC stream

        uoc_6 = core_l1_filters + [chem_or] + [phys_or] + [math1_or] + [math2_or] + core_l2_filters + [mathl2_or] + [sci2_or] + core_l3_filters + core_l4_filters
        for f in uoc_6:
            h.add_degree_reqs(BINF, year, f, 6)

        uoc_4 = hons_filters
        for f in uoc_4:
            h.add_degree_reqs(BINF, year, f, 4)

        h.add_degree_reqs(BINF, year, disc_filter, 12 + 12, 'Discipline Electives')

        # 12 UOC General Education
        h.add_degree_reqs(BINF, year, gen_filter, 12)

        # 12 UOC Electives (Foundational Disciplinary or Disciplinary Knowledge Courses)
        # "Discipline Elective List"
        h.add_degree_notes(BINF, year, 'Discipline Electives include: any level 3, 4, 6, 9 COMP course; any level 3 BABS course; any level 3 BIOC course; any level 3 MICR course; ENGG3060')

        # level 3 maturity requirements
        # students must complete 42 UOC before taking any level 3 course
        h.add_degree_notes(BINF, year, 'Students must have completed 42 UOC before taking any level 3 course.')

        # level 4 maturity requirements
        # students must complete 102 UOC before taking any level 4 course
        h.add_degree_notes(BINF, year, 'Students must have completed 102 UOC before taking any level 4 course.')

        # 60 days of Industrial Training 
        h.add_degree_notes(BINF, year, 'Students must have completed a minimum of 60 days of Industrial Training to graduate. Industrial training must be undertaken concurrently with enrolment in the program.')       

        # total_UOC = 192
        h.add_degree_reqs(BINF, year, None, 192)

def insert_compeng_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/COMPBH
    h = Helper(dbaddr=db)

    # ===> start filters needed

    # level 1
    core_l1_filters = h.spec_courses_to_filters(['COMP1511', 'COMP1521', 'COMP1531', 'ELEC1111', 'ENGG1000'])

    math1_filters = h.spec_courses_to_filters(['MATH1131', 'MATH1141'])
    math1_or = h.combine_course_filters('or', math1_filters)

    math2_filters = h.spec_courses_to_filters(['MATH1231', 'MATH1241'])
    math2_or = h.combine_course_filters('or', math2_filters)

    phys1_filters = h.spec_courses_to_filters(['PHYS1121', 'PHYS1131'])
    phys1_or = h.combine_course_filters('or', phys1_filters)

    phys2_filters = h.spec_courses_to_filters(['PHYS1221', 'PHYS1231'])
    phys2_or = h.combine_course_filters('or', phys2_filters)

    # level 2
    core_l2_filters = h.spec_courses_to_filters(['COMP2511', 'COMP2521', 'DESN2000', 'ELEC2133',
        'ELEC2134', 'MATH2069', 'MATH2099'])

    # level 3
    core_l3_filters = h.spec_courses_to_filters(['COMP3211', 'COMP3222', 'COMP3231', 'COMP3601'])

    # level 4
    core_l4_filters = h.spec_courses_to_filters(['COMP4601', 'COMP4920'])

    # 4 UOC
    hons = h.spec_courses_to_filters(['COMP4951', 'COMP4952', 'COMP4953'])

    # discipline electives


    gen_filter = h.add_course_filter('gen')
    # ===> end filters needed
    level3 = h.add_course_filter('level', level=3)
    level4 = h.add_course_filter('level', level=4)
    level6 = h.add_course_filter('level', level=6)
    level9 = h.add_course_filter('level', level=9)

    # any level 3, 4, 6, 9 computer science
    comp = h.add_course_filter('field', field_code='COMP')
    comp_levels = h.combine_course_filters('or', [level3, level4, level6, level9])
    comp_disc = h.combine_course_filters('and', [comp, comp_levels])

    # ENGG3060, 3 UOC
    maker = h.add_course_filter('spec', min_mark=50, course='ENGG3060') 

    disc_filter = h.combine_course_filters('or', [comp_disc, maker])

    print('==> Inserting Degree Requirements for COMPBH Degree')

    COMP = '3707 COMPBH'

    print('Inserting degree...')
    h.add_degree('Engineering (Honours) (Computer)', 'Faculty of Engineering', 4, COMP)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, COMP)

        # 168 UOC stream
        uoc_6 = core_l1_filters + [math1_or] + [math2_or] + [phys1_or] + [phys2_or] + core_l2_filters + core_l3_filters + core_l4_filters
        for f in uoc_6:
            h.add_degree_reqs(COMP, year, f, 6)

        uoc_4 = hons 
        for f in uoc_4:
            h.add_degree_reqs(COMP, year, f, 4)

        h.add_degree_reqs(COMP, year, disc_filter, 24 + 12, 'Discipline Electives')

        # 12 UOC General Education
        h.add_degree_reqs(COMP, year, gen_filter, 12)

        # 12 UOC Electives (Foundational Disciplinary or Disciplinary Knowledge Courses)
        # "Discipline Elective List"
        h.add_degree_notes(COMP, year, 'Discipline Electives include: any level 3, 4, 6, 9 COMP course; ENGG3060')

        # level 3 maturity requirements
        # students must complete 42 UOC before taking any level 3 course
        h.add_degree_notes(COMP, year, 'Students must have completed 42 UOC before taking any level 3 course.')

        # level 4 maturity requirements
        # students must complete 102 UOC before taking any level 4 course
        h.add_degree_notes(COMP, year, 'Students must have completed 102 UOC before taking any level 4 course.')

        # level 4 UOC minimum
        h.add_degree_notes(COMP, year, 'Students must complete a minimum of 36 UOC of level 4 courses, including core courses, and at least 12 UOC of level 4 Discipline Electives')

        # 60 days of Industrial Training 
        h.add_degree_notes(COMP, year, 'Students must have completed a minimum of 60 days of Industrial Training to graduate. Industrial training must be undertaken concurrently with enrolment in the program.')       

        # total_UOC = 192
        h.add_degree_reqs(COMP, year, None, 192)

def insert_fins_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/FINSA1
    h = Helper(dbaddr=db)

    # ===> start filters needed
    bus_core = h.spec_courses_to_filters(['ACCT1501', 'ECON1101', 'ECON1203', 'MGMT1001'])

    flex_core = h.spec_courses_to_filters(['ACCT1511', 'COMM1000', 'COMM1822', 'ECON1102',
        'INFS1602', 'MARK1012', 'MGMT1101', 'TABL1710'])
    flex_or = h.combine_course_filters('or', flex_core)

    free_filter = h.add_course_filter('free')
    gen_filter = h.add_course_filter('gen')

    fins_core = h.spec_courses_to_filters(['FINS1612', 'FINS1613', 'FINS2624', 'FINS3616'])

    presc_elec = h.spec_courses_to_filters(['ACCT3563', 'COMM2222', 'COMM3020', 'COMM3030',
        'COMM3101', 'COMM3202', 'FINS2622', 'FINS2643', 'FINS3623', 'FINS3625', 'FINS3626',
        'FINS3630', 'FINS3631', 'FINS3633', 'FINS3634', 'FINS3635', 'FINS3636', 'FINS3637', 
        'FINS3640', 'FINS3641', 'FINS3644', 'FINS3650', 'FINS3655', 'FINS3666', 'FINS3775',
        'FINS3645', 'FINS3646', 'FINS3647', 'FINS3648'])
    # presc_one = h.spec_courses_to_filters(['FINS3645', 'FINS3646', 'FINS3647', 'FINS3648'])
    presc_filter = h.combine_course_filters('or', presc_elec)

    # ===> end filters needed
 
    print('==> Inserting Degree Requirements for FINSA1 Degree')

    FINS = '3502 FINSA1'

    print('Inserting degree...')
    h.add_degree('Commerce (Finance)', 'Faculty of Business', 3, FINS)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, FINS)

        # business core courses, 24 UOC (all of them)
        for f in bus_core:
            h.add_degree_reqs(FINS, year, f, 6)

        # flexible core courses, 24 UOC
        h.add_degree_reqs(FINS, year, flex_or, 24)

        # business major = 48 UOC in stream and at least 18 UOC in level 3
        for f in fins_core:
            h.add_degree_reqs(FINS, year, f, 6)

        # prescribed electives
        h.add_degree_reqs(FINS, year, presc_filter, 24, 'Prescribed Electives')

        # 36 UOC free electives (GEN courses cannot count as free elective)
        h.add_degree_reqs(FINS, year, free_filter, 36)

        # 12 UOC General Education
        h.add_degree_reqs(FINS, year, gen_filter, 12)

        # total_UOC = 144
        h.add_degree_reqs(FINS, year, None, 144)

        h.add_degree_notes(FINS, year, 'Prescribed Electives include: ACCT3563, COMM2222, COMM3020, COMM3030, COMM3101, COMM3202, FINS2622, FINS2643, FINS3623, FINS3625, FINS3626, FINS3630, FINS3631, FINS3633, FINS3634, FINS3635, FINS3636, FINS3637, FINS3640, FINS3641, FINS3644, FINS3650, FINS3655, FINS3666, FINS3775. You can also choose ONE of the following: FINS3645, FINS3646, FINS3647, FINS3648. At least 2 of your prescribed electives must be level 3.')

        # program limit of 60 UOC level 1 courses
        h.add_degree_notes(FINS, year, 'Students must complete a maximum of 60 UOC of level 1 courses, excluding level 1 courses completed as part of the General Education requirement in Dual Programs.')

        # general education maturity
        h.add_degree_notes(FINS, year, 'Students must complete at least 48 UOC before enrolling in General Education courses.')

        # level 2 and 3 maturity requirements
        h.add_degree_notes(FINS, year, 'Students must have completed 24 UOC before taking any level 2 courses.')
        h.add_degree_notes(FINS, year, 'Students must have completed 48 UOC before taking any level 3 courses.')

        # minimum faculty UOC, 96 UOC in business school
        h.add_degree_notes(FINS, year, 'Students must complete a minimum of 96 UOC of any course offered by UNSW Business School.')



def insert_acct_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/ACCTA1
    h = Helper(dbaddr=db)

    # ===> start filters needed
    bus_core = h.spec_courses_to_filters(['ECON1101', 'ECON1203', 'MGMT1001'])

    flex_core = h.spec_courses_to_filters(['COMM1000', 'COMM1822', 'ECON1102', 'FINS1613',
        'INFS1602', 'MARK1012', 'MGMT1101', 'TABL1710'])
    flex_or = h.combine_course_filters('or', flex_core)

    free_filter = h.add_course_filter('free')
    gen_filter = h.add_course_filter('gen')

    acct_core = h.spec_courses_to_filters(['ACCT1501', 'ACCT1511', 'ACCT2522', 'ACCT2542', 'ACCT3563'])

    presc = h.spec_courses_to_filters(['ACCT2507', 'ACCT2672', 'ACCT3583', 'ACCT3601', 'ACCT3610',
        'ACCT3708', 'COMM2222', 'COMM2233', 'COMM3020', 'COMM3030', 'COMM3101', 'COMM3202', 'FINS3626',
        'TABL2741', 'TABL3033'])
    presc_or = h.combine_course_filters('or', presc)

    # school of business
    acct = h.add_course_filter('field', field_code='ACCT')
    fins = h.add_course_filter('field', field_code='FINS')
    econ = h.add_course_filter('field', field_code='ECON')
    infs = h.add_course_filter('field', field_code='INFS')
    mgmt = h.add_course_filter('field', field_code='MGMT')
    mark = h.add_course_filter('field', field_code='MARK')
    risk = h.add_course_filter('field', field_code='RISK')
    tabl = h.add_course_filter('field', field_code='TABL')
    comm = h.add_course_filter('field', field_code='COMM')
    # actl = h.add_course_filter('field', field_code='ACTL') # TODO add in
    bus = h.combine_course_filters('or', [acct, fins, econ, infs, mgmt, mark, risk, tabl, comm])
    # ===> end filters needed
 
    print('==> Inserting Degree Requirements for ACCTA1 Degree')

    ACCT = '3502 ACCTA1'

    print('Inserting degree...')
    h.add_degree('Commerce (Accounting)', 'Faculty of Business', 3, ACCT)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, ACCT)

        # business core courses, 24 UOC (all of them)
        for f in bus_core:
            h.add_degree_reqs(ACCT, year, f, 6)

        # flexible core courses, 24 UOC
        h.add_degree_reqs(ACCT, year, flex_or, 24)

        # business major = 48 UOC in stream and at least 18 UOC in level 3
        for f in acct_core:
            h.add_degree_reqs(ACCT, year, f, 6)

        h.add_degree_reqs(ACCT, year, presc_or, 18, 'Prescribed Electives')

        # one school of business elective due to overlap in business core and ACCT core
        h.add_degree_reqs(ACCT, year, bus, 6, 'UNSW Business School Course')

        # 36 UOC free electives (GEN courses cannot count as free elective)
        h.add_degree_reqs(ACCT, year, free_filter, 36)

        # 12 UOC General Education
        h.add_degree_reqs(ACCT, year, gen_filter, 12)

        # total_UOC = 144
        h.add_degree_reqs(ACCT, year, None, 144)

        h.add_degree_notes(ACCT, year, 'Prescribed Electives include: ACCT2507, ACCT2672, ACCT3583, ACCT3601, ACCT3610, ACCT3708, COMM2222, COMM2233, COMM3020, COMM3030, COMM3101, COMM3202, FINS3626, TABL2741, TABL3033. At least 12 UOC must be at level 3.')

        h.add_degree_notes(ACCT, year, 'UNSW Business School Courses include those with fields: ACCT, ACTL, COMM, ECON, FINS, INFS, MARK, MGMT, RISK, TABL.')

        # program limit of 60 UOC level 1 courses
        h.add_degree_notes(ACCT, year, 'Students must complete a maximum of 60 UOC of level 1 courses, excluding level 1 courses completed as part of the General Education requirement in Dual Programs.')

        # general education maturity
        h.add_degree_notes(ACCT, year, 'Students must complete at least 48 UOC before enrolling in General Education courses.')

        # level 2 and 3 maturity requirements
        h.add_degree_notes(ACCT, year, 'Students must have completed 24 UOC before taking any level 2 courses.')
        h.add_degree_notes(ACCT, year, 'Students must have completed 48 UOC before taking any level 3 courses.')

        # minimum faculty UOC, 96 UOC in business school
        h.add_degree_notes(ACCT, year, 'Students must complete a minimum of 96 UOC of any course offered by UNSW Business School.')

# def insert_fins_degree_requirements(db='university.db', start_year=2020, end_year=2021):
#     # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/FINSA1
#     h = Helper(dbaddr=db)

#     # ===> start filters needed
#     bus_core = h.spec_courses_to_filters(['ACCT1501', 'ECON1101', 'ECON1203', 'MGMT1001'])

#     flex_core = h.spec_courses_to_filters(['ACCT1511', 'COMM1000', 'COMM1822', 'ECON1102', 'FINS1613',
#         'INFS1602', 'MARK1012', 'MGMT1101', 'TABL1710'])
#     flex_or = h.combine_course_filters('or', flex_core)

#     free_filter = h.add_course_filter('free')
#     gen_filter = h.add_course_filter('gen')
#     # ===> end filters needed
 
#     print('==> Inserting Degree Requirements for FINSA1 Degree')

#     FINS = '3502 FINSA1'

#     print('Inserting degree...')
#     h.add_degree('Commerce (Finance)', 'Faculty of Business', 3, FINS)

#     print('Inserting degree offerings and requirements...')
#     for year in range(start_year, end_year + 1):
#         print(f'... year {year}')
#         h.add_degree_offering(year, FINS)

#         # business core courses, 24 UOC (all of them)
#         for f in bus_core:
#             h.add_degree_reqs(FINS, year, f, 6)

#         # flexible core courses, 24 UOC
#         h.add_degree_reqs(FINS, year, flex_or, 24)

#         # business major = 48 UOC in stream and at least 18 UOC in level 3

#         # 36 UOC free electives (GEN courses cannot count as free elective)
#         h.add_degree_reqs(FINS, year, free_filter, 36)

#         # 12 UOC General Education
#         h.add_degree_reqs(FINS, year, gen_filter, 12)

#         # total_UOC = 144
#         h.add_degree_reqs(FINS, year, None, 144)

#         # program limit of 60 UOC level 1 courses
#         h.add_degree_notes(FINS, year, 'Students must complete a maximum of 60 UOC of level 1 courses, excluding level 1 courses completed as part of the General Education requirement in Dual Programs.')

#         # general education maturity
#         h.add_degree_notes(FINS, year, 'Students must complete at least 48 UOC before enrolling in General Education courses.')

#         # level 2 and 3 maturity requirements
#         h.add_degree_notes(FINS, year, 'Students must have completed 24 UOC before taking any level 2 courses.')
#         h.add_degree_notes(FINS, year, 'Students must have completed 48 UOC before taking any level 3 courses.')

#         # minimum faculty UOC, 96 UOC in business school
#         h.add_degree_notes(FINS, year, 'Students must complete a minimum of 96 UOC of any course offered by UNSW Business School.')


def insert_stat_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/programs/2020/3970?q=science&ct=course
    h = Helper(dbaddr=db)

    # ===> course filters
    math1_opts = h.spec_courses_to_filters(['MATH1131', 'MATH1141'])
    math1_or = h.combine_course_filters('or', math1_opts)

    math2_opts = h.spec_courses_to_filters(['MATH1231', 'MATH1241'])
    math2_or = h.combine_course_filters('or', math2_opts)

    calc_opts = h.spec_courses_to_filters(['MATH2011', 'MATH2111'])
    calc_or = h.combine_course_filters('or', calc_opts)

    alg_opts = h.spec_courses_to_filters(['MATH2501', 'MATH2601'])
    alg_or = h.combine_course_filters('or', alg_opts)

    stat_opts = h.spec_courses_to_filters(['MATH2801', 'MATH2901'])
    stat_or = h.combine_course_filters('or', stat_opts)

    lin_opts = h.spec_courses_to_filters(['MATH2831', 'MATH2931'])
    lin_or = h.combine_course_filters('or', lin_opts)

    statmodel = h.spec_courses_to_filters(['MATH3821'])

    stoch_opts = h.spec_courses_to_filters(['MATH3801', 'MATH3901'])
    stoch_or = h.combine_course_filters('or', stoch_opts)

    inf_opts = h.spec_courses_to_filters(['MATH3811', 'MATH3911'])
    inf_or = h.combine_course_filters('or', inf_opts)

    math_elec = h.spec_courses_to_filters(['MATH3831', 'MATH3841', 'MATH3851', 'MATH3871'])
    elec_or = h.combine_course_filters('or', math_elec)

    sci_elec = ['ANAT', 'AVEN', 'AVIA', 'AVIF', 'AVIG', 'BABS', 'BEES', 'BIOC', 'BIOS', 'BIOT', 
        'CHEM', 'CLIM', 'COMP', 'FOOD', 'GEOS', 'MATH', 'MATS', 'MICR', 'MSCI', 'NEUR', 'OPTM', 
        'PATH', 'PHAR', 'PHSL', 'PHYS', 'PSYC', 'SCIF', 'SOMS', 'VISN']
    field_filters = []
    for field in sci_elec:
        field_filters.append(h.add_course_filter('field', field_code=field))
    sci_or = h.combine_course_filters('or', field_filters)

    gen_filter = h.add_course_filter('gen')
    free_filter = h.add_course_filter('free')
    # ===> end course filters

    print('==> Inserting Degree Requirements for MATHT1 Degree')
    STAT = '3970 MATHT1'

    print('Inserting degree...')
    h.add_degree('Science (Statistics)', 'Faculty of Science', 3, STAT)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, STAT)

        # 108 UOC science courses: BS major + Science electives

        # BS major, stat = 60 UOC
        uoc_6 = [math1_or, math2_or, calc_or, alg_or, stat_or, lin_or, stoch_or, inf_or, elec_or] + statmodel
        for f in uoc_6:
            h.add_degree_reqs(STAT, year, f, 6)

        # science electives, at least 12 UOC (however many to make up 108)
        h.add_degree_reqs(STAT, year, sci_or, 108 - 60, 'Science Electives')

        # 24 UOC free electives
        h.add_degree_reqs(STAT, year, free_filter, 24)

        # 12 UOC general education
        h.add_degree_reqs(STAT, year, gen_filter, 12)

        h.add_degree_reqs(STAT, year, None, 144)

        # notes
        h.add_degree_notes(STAT, year, 'Science Electives include courses with the following field codes: ANAT, AVEN, AVIA, AVIF, AVIG, BABS, BEES, BIOC, BIOS, BIOT, CHEM, CLIM, COMP, FOOD, GEOS, MATH, MATS, MICR, MSCI, NEUR, OPTM, PATH, PHAR, PHSL, PHYS, PSYC, SCIF, SOMS, VISN.')

        h.add_degree_notes(STAT, year, 'GEN# courses cannot count towards the free elective component, or towards science core courses or science electives in the program. Any exceptions to these rules must be approved by the Associate Dean (Academic Programs) or nominee.')

        h.add_degree_notes(STAT, year, 'Students may not take the following course as general education: any COMP, FOOD, SOMS, GENS course; any course by the Faculty of Science.')

        h.add_degree_notes(STAT, year, 'Students must complete a minimum of 24 UOC of level 1 courses by the Faculty of Science.')

        h.add_degree_notes(STAT, year, 'A maximum of 72 UOC of level 1 courses can be taken, including any General Education or mainstream Level 1 course taken to fulfill either the General Education or the Free Elective requirement.')

        h.add_degree_notes(STAT, year, 'Students must have completed 30 UOC before taking any level 2 course.')

        h.add_degree_notes(STAT, year, 'Students must have completed 72 UOC before taking any level 3, 6 courses.')

def insert_psyc_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/PSYCA1
    h = Helper(dbaddr=db)

    # ===> course filters
    core_l1 = h.spec_courses_to_filters(['PSYC1001', 'PSYC1011', 'PSYC1111'])

    core_l2 = h.spec_courses_to_filters(['PSYC2001', 'PSYC2061', 'PSYC2071', 'PSYC2081', 'PSYC2101'])

    core_l3 = h.spec_courses_to_filters(['PSYC3001', 'PSYC3011'])

    l3_presc = h.spec_courses_to_filters(['PSYC3051', 'PSYC3121', 'PSYC3211', 'PSYC3221', 'PSYC3241', 
        'PSYC3301', 'PSYC3311', 'PSYC3331', 'PSYC3341', 'PSYC3361', 'PSYC3371'])
    presc_or = h.combine_course_filters('or', l3_presc)

    sci_elec = ['ANAT', 'AVEN', 'AVIA', 'AVIF', 'AVIG', 'BABS', 'BEES', 'BIOC', 'BIOS', 'BIOT', 
        'CHEM', 'CLIM', 'COMP', 'FOOD', 'GEOS', 'MATH', 'MATS', 'MICR', 'MSCI', 'NEUR', 'OPTM', 
        'PATH', 'PHAR', 'PHSL', 'PHYS', 'PSYC', 'SCIF', 'SOMS', 'VISN']
    field_filters = []
    for field in sci_elec:
        field_filters.append(h.add_course_filter('field', field_code=field))
    sci_or = h.combine_course_filters('or', field_filters)

    gen_filter = h.add_course_filter('gen')
    free_filter = h.add_course_filter('free')
    # ===> end course filters

    print('==> Inserting Degree Requirements for PSYCA1 Degree')
    PSYC = '3970 PSYCA1'

    print('Inserting degree...')
    h.add_degree('Science (Psychology)', 'Faculty of Science', 3, PSYC)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, PSYC)

        # 108 UOC science courses: BS major + Science electives

        # BS major: 78 UOC
        uoc_6 = core_l1 + core_l2 + core_l3
        for f in uoc_6: 
            h.add_degree_reqs(PSYC, year, f, 6)

        h.add_degree_reqs(PSYC, year, presc_or, 18)

        # science electives, at least 12 UOC (however many to make up 108)
        h.add_degree_reqs(PSYC, year, sci_or, 108 - 78, 'Science Electives')

        # 24 UOC free electives
        h.add_degree_reqs(PSYC, year, free_filter, 24)

        # 12 UOC general education
        h.add_degree_reqs(PSYC, year, gen_filter, 12)

        h.add_degree_reqs(PSYC, year, None, 144)

        # notes
        h.add_degree_notes(PSYC, year, 'Science Electives include courses with the following field codes: ANAT, AVEN, AVIA, AVIF, AVIG, BABS, BEES, BIOC, BIOS, BIOT, CHEM, CLIM, COMP, FOOD, GEOS, MATH, MATS, MICR, MSCI, NEUR, OPTM, PATH, PHAR, PHSL, PHYS, PSYC, SCIF, SOMS, VISN.')

        h.add_degree_notes(PSYC, year, 'Prescribed Level 3 Psychology Electives include: PSYC3051, PSYC3121, PSYC3211, PSYC3221, PSYC3241, PSYC3301, PSYC3311, PSYC3331, PSYC3341, PSYC3361, PSYC3371.')

        h.add_degree_notes(PSYC, year, 'Students must include at least one course from elective list A: PSYC3051, PSYC3211, PSYC3221, PSYC3241, PSYC3311, PSYC3371.')

        h.add_degree_notes(PSYC, year, 'Students must include at least on course from elective list B: PSYC3121, PSYC3202, PSYC3301, PSYC3331, PSYC3341, PSYC3361.')

        h.add_degree_notes(PSYC, year, 'GEN# courses cannot count towards the free elective component, or towards science core courses or science electives in the program. Any exceptions to these rules must be approved by the Associate Dean (Academic Programs) or nominee.')

        h.add_degree_notes(PSYC, year, 'Students may not take the following course as general education: any COMP, FOOD, SOMS, GENS course; any course by the Faculty of Science.')

        h.add_degree_notes(PSYC, year, 'Students must complete a minimum of 24 UOC of level 1 courses by the Faculty of Science.')

        h.add_degree_notes(PSYC, year, 'A maximum of 72 UOC of level 1 courses can be taken, including any General Education or mainstream Level 1 course taken to fulfill either the General Education or the Free Elective requirement.')

        h.add_degree_notes(PSYC, year, 'Students must have completed 30 UOC before taking any level 2 course.')

        h.add_degree_notes(PSYC, year, 'Students must have completed 72 UOC before taking any level 3, 6 courses.')

def insert_bio_degree_requirements(db='university.db', start_year=2020, end_year=2021):
    # https://www.handbook.unsw.edu.au/undergraduate/specialisations/2020/BIOSJ1
    h = Helper(dbaddr=db)

    # ===> course filters
    core_l1 = h.spec_courses_to_filters(['BABS1201', 'BIOS1101', 'BIOS1301', 'MATH1041'])

    core_l2 = h.spec_courses_to_filters(['BEES2041'])

    gen_opts = h.spec_courses_to_filters(['BABS2204', 'BABS2264'])
    gen_or = h.combine_course_filters('or', gen_opts)

    l2_presc_opts = h.spec_courses_to_filters(['BIOS2011', 'BIOS2031', 'BIOS2051', 'BIOS2061'])
    l2_presc = h.combine_course_filters('or', l2_presc_opts)

    l3_presc_opts = h.spec_courses_to_filters(['BIOS3011', 'BIOS3061', 'BIOS3081', 'BIOS3161',
        'BIOS3171', 'BIOS3221', 'BIOS3601', 'BIOS6671', 'GEOS3911'])
    l3_presc = h.combine_course_filters('or', l3_presc_opts)

    sci_elec = ['ANAT', 'AVEN', 'AVIA', 'AVIF', 'AVIG', 'BABS', 'BEES', 'BIOC', 'BIOS', 'BIOT', 
        'CHEM', 'CLIM', 'COMP', 'FOOD', 'GEOS', 'MATH', 'MATS', 'MICR', 'MSCI', 'NEUR', 'OPTM', 
        'PATH', 'PHAR', 'PHSL', 'PHYS', 'PSYC', 'SCIF', 'SOMS', 'VISN']
    field_filters = []
    for field in sci_elec:
        field_filters.append(h.add_course_filter('field', field_code=field))
    sci_or = h.combine_course_filters('or', field_filters)

    gen_filter = h.add_course_filter('gen')
    free_filter = h.add_course_filter('free')
    # ===> end course filters

    print('==> Inserting Degree Requirements for BIOSJ1 Degree')
    BIO = '3970 BIOSJ1'

    print('Inserting degree...')
    h.add_degree('Science (Biology)', 'Faculty of Science', 3, BIO)

    print('Inserting degree offerings and requirements...')
    for year in range(start_year, end_year + 1):
        print(f'... year {year}')
        h.add_degree_offering(year, BIO)

        # 108 UOC science courses: BS major + Science electives

        # BS major: 78
        uoc_6 = core_l1 + core_l2 + [gen_or]
        for f in uoc_6:
            h.add_degree_reqs(BIO, year, f, 6)

        h.add_degree_reqs(BIO, year, l2_presc, 12)

        h.add_degree_reqs(BIO, year, l3_presc, 30)

        # science electives, at least 12 UOC (however many to make up 108)
        h.add_degree_reqs(BIO, year, sci_or, 108 - 78, 'Science Electives')

        # 24 UOC free electives
        h.add_degree_reqs(BIO, year, free_filter, 24)

        # 12 UOC general education
        h.add_degree_reqs(BIO, year, gen_filter, 12)

        h.add_degree_reqs(BIO, year, None, 144)

        # notes
        h.add_degree_notes(BIO, year, 'Science Electives include courses with the following field codes: ANAT, AVEN, AVIA, AVIF, AVIG, BABS, BEES, BIOC, BIOS, BIOT, CHEM, CLIM, COMP, FOOD, GEOS, MATH, MATS, MICR, MSCI, NEUR, OPTM, PATH, PHAR, PHSL, PHYS, PSYC, SCIF, SOMS, VISN.')

        h.add_degree_notes(BIO, year, 'GEN# courses cannot count towards the free elective component, or towards science core courses or science electives in the program. Any exceptions to these rules must be approved by the Associate Dean (Academic Programs) or nominee.')

        h.add_degree_notes(BIO, year, 'Students may not take the following course as general education: any COMP, FOOD, SOMS, GENS course; any course by the Faculty of Science.')

        h.add_degree_notes(BIO, year, 'Students must complete a minimum of 24 UOC of level 1 courses by the Faculty of Science.')

        h.add_degree_notes(BIO, year, 'A maximum of 72 UOC of level 1 courses can be taken, including any General Education or mainstream Level 1 course taken to fulfill either the General Education or the Free Elective requirement.')

        h.add_degree_notes(BIO, year, 'Students must have completed 30 UOC before taking any level 2 course.')

        h.add_degree_notes(BIO, year, 'Students must have completed 72 UOC before taking any level 3, 6 courses.')

# def insert_stat_degree_requirements(db='university.db', start_year=2020, end_year=2021):
#     # https://www.handbook.unsw.edu.au/undergraduate/programs/2020/3970?q=science&ct=course
#     h = Helper(dbaddr=db)

#     # ===> course filters

#     sci_elec = ['ANAT', 'AVEN', 'AVIA', 'AVIF', 'AVIG', 'BABS', 'BEES', 'BIOC', 'BIOS', 'BIOT', 
#         'CHEM', 'CLIM', 'COMP', 'FOOD', 'GEOS', 'MATH', 'MATS', 'MICR', 'MSCI', 'NEUR', 'OPTM', 
#         'PATH', 'PHAR', 'PHSL', 'PHYS', 'PSYC', 'SCIF', 'SOMS', 'VISN']
#     field_filters = []
#     for field in sci_elec:
#         field_filters.append(h.add_course_filter('field', field_code=field))
#     sci_or = h.combine_course_filters('or', field_filters)

#     gen_filter = h.add_course_filter('gen')
#     free_filter = h.add_course_filter('free')
#     # ===> end course filters

#     print('==> Inserting Degree Requirements for MATHT1 Degree')
#     STAT = '3970 MATHT1'

#     print('Inserting degree...')
#     h.add_degree('Science (Statistics)', 'Faculty of Science', 3, STAT)

#     print('Inserting degree offerings and requirements...')
#     for year in range(start_year, end_year + 1):
#         print(f'... year {year}')
#         h.add_degree_offering(year, STAT)

#         # 108 UOC science courses: BS major + Science electives

#         # TODO BS major

#         # TODO science electives, at least 12 UOC (however many to make up 108)
#         h.add_degree_reqs(STAT, year, sci_or, 12, 'Science Electives')

#         # 24 UOC free electives
#         h.add_degree_reqs(STAT, year, free_filter, 24)

#         # 12 UOC general education
#         h.add_degree_reqs(STAT, year, gen_filter, 12)

#         h.add_degree_reqs(STAT, year, None, 144)

#         # notes
#         h.add_degree_notes(STAT, year, 'Science Electives include courses with the following field codes: ANAT, AVEN, AVIA, AVIF, AVIG, BABS, BEES, BIOC, BIOS, BIOT, CHEM, CLIM, COMP, FOOD, GEOS, MATH, MATS, MICR, MSCI, NEUR, OPTM, PATH, PHAR, PHSL, PHYS, PSYC, SCIF, SOMS, VISN.')

#         h.add_degree_notes(STAT, year, 'GEN# courses cannot count towards the free elective component, or towards science core courses or science electives in the program. Any exceptions to these rules must be approved by the Associate Dean (Academic Programs) or nominee.')

#         h.add_degree_notes(STAT, year, 'Students may not take the following course as general education: any COMP, FOOD, SOMS, GENS course; any course by the Faculty of Science.')

#         h.add_degree_notes(STAT, year, 'Students must complete a minimum of 24 UOC of level 1 courses by the Faculty of Science.')

#         h.add_degree_notes(STAT, year, 'A maximum of 72 UOC of level 1 courses can be taken, including any General Education or mainstream Level 1 course taken to fulfill either the General Education or the Free Elective requirement.')

#         h.add_degree_notes(STAT, year, 'Students must have completed 30 UOC before taking any level 2 course.')

#         h.add_degree_notes(STAT, year, 'Students must have completed 72 UOC before taking any level 3, 6 courses.')

if __name__ == '__main__':
        # Computer Science (3778) (COMPA1) courses
        # compsci_course_reqs()
        # insert_sessions()
        # insert_course_offerings()
        # insert_compsci_degree_requirements()
        insert_seng_degree_requirements()

        pass
