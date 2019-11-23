'''
Helper class to help insert information into our database
'''

import sqlite3

class Helper:
    def __init__(self, dbaddr='university.db'):
        self.db = sqlite3.connect(dbaddr)
        self.cursor = self.db.cursor()
        self.cursor.row_factory = sqlite3.Row

    def get_course_id(self, course):
        '''
        <course> a string like 'COMP1511'

        Returns the id of the Course entry corresponding to this course

        If the course does not exist, adds a dummy course (for the purpose of courses in
        previous years)
        '''
        letter_code = course[:4]
        number_code = course[4:]

        # find the course id
        self.cursor.execute('select id from courses where letter_code = ? and number_code = ?',
            (letter_code, number_code))
        result = self.cursor.fetchone()
        if result is None:
            print(f'Adding course {course} because it doesn\'t exist in the database/must be from earlier years')

            course_id = self.cursor.execute('''insert into Courses(letter_code, number_code, level, units,
        finished, faculty, name) values(?, ?, ?, ?, ?, ?, ?)''', (letter_code, number_code,
        number_code[0], 6, 0, 'Unkown Faculty', 'Unknown Course Name'))
            # find the course id
            self.cursor.execute('select id from courses where letter_code = ? and number_code = ?',
            (letter_code, number_code))

            result = self.cursor.fetchone()

        course_id = result[0]

        return course_id

    def has_entry(self, check_msg, values_tuple):
        '''
        Check if the given query returns results
        True if entry exists in db, otherwise False
        '''
        # print(f'... has_entry: check_msg = {check_msg}, values_tuple = {values_tuple}')
        self.cursor.execute(check_msg, values_tuple)
        results = self.cursor.fetchall()

        if len(results) == 0:
            return False, None
        else:
            if 'id' in results[0].keys():
                item_id = results[0]['id']
            elif 'degree_id' in results[0].keys():
                # DegreeOfferings table only has 'degree_id' not 'id'
                item_id = results[0]['degree_id']
            else:
                # some tables don't have a separate id
                item_id = None
            return True, item_id

    def safe_insert(self, msg, values, unique_values, type_id=None):
        '''
        Safely inserts an entry. Calls self.check_exists() first.
        Then if not exists calls self.insert().
        <msg> is the sql insert statement in form 'INSERT INTO <table>(...'
        <values> is the tuple of values corresponding to ? in <msg>
        <unique_values> is a tuple of values needed to check this
        <table> is either 'req', 'filters', or None for types of tables with type_id arguments
        entry is unique for the given table. Requires knowledge of
        unique() declaratoins in schema.sql.
        '''
        # parse out the table name from msg
        table = (msg.split()[2]).split('(')[0]

        # see if the data already exists in the table
        # if so, grab the id of that element to return
        exists, inserted_id = self.check_exists(table, unique_values, type_id)

        if not exists:
            inserted_id = self.insert(msg, values)

        return inserted_id

    def check_exists(self, table, values, type_id=None):
        '''
        Checks if the entry exists in the given table name.
        Values is a list of tuple values that should correspond
        to the order of unique() statements in schema.sql. 

        Can't really make it more extensible as knowledge about which
        variables are needed for uniqueness is required. 

        <type_id> is for CourseRequirements
        '''
        exists = False
        item_id = None

        if table == 'Degrees':
            check = 'SELECT id FROM Degrees where id = ?'
        elif table == 'DegreeOfferings':
            check = 'SELECT year, degree_id FROM DegreeOfferings where year = ? and degree_id = ?'
        elif table == 'Courses':
            check = 'SELECT letter_code, number_code, id FROM courses where letter_code = ? and number_code = ?'
        elif table == 'Sessions':
            check = 'SELECT year, term FROM Sessions where year = ? and term = ?'
        elif table == 'CourseFilters':

            if type_id is None:
                raise Exception('You need to specify a type_id for CourseFilters check')

            if type_id == 1:
                # specific course filter
                check = 'SELECT type_id, min_mark, course_id, id FROM CourseFilters where type_id = ? and min_mark = ? and course_id = ?'
            elif type_id == 2:
                # gened filter
                check = 'SELECT type_id, id FROM CourseFilters where type_id = ?'
            elif type_id == 3:
                # field filter
                check = 'SELECT type_id, field_code, id FROM CourseFilters where type_id = ? and field_code = ?'
            elif type_id == 4:
                # level filter
                check = 'SELECT type_id, level, id FROM CourseFilters where type_id = ? and level = ?'
            elif type_id == 5:
                # free elective filter
                check = 'SELECT type_id, id FROM CourseFilters where type_id = ?'
            # TODO not checking AND or OR requirements yet cuz complicated

        elif table == 'CourseFilterHierarchies':
            check = 'SELECT parent_id, child_id from CourseFilterHierarchies where parent_id = ? and child_id = ?'
        elif table == 'CourseRequirements':

            if type_id is None:
                raise Exception('You need to specify a type_id for CourseRequirements check')

            if type_id == 1:
                # completed
                check = 'SELECT type_id, min_mark, course_id, id from CourseRequirements WHERE type_id = ? and min_mark = ? and course_id = ?'
            elif type_id == 2:
                # current degree
                check = 'SELECT type_id, degree_id, id from CourseRequirements WHERE type_id = ? and degree_id = ?'
            elif type_id == 3:
                # year requirement
                check = 'SELECT type_id, year, id from CourseRequirements WHERE type_id = ? and year = ?'
            elif type_id == 4:
                # UOC requirement
                check = 'SELECT type_id, uoc_amount_required, uoc_min_level, uoc_subject, uoc_course_filter, id FROM CourseRequirements WHERE type_id = ? and uoc_amount_required = ? and uoc_min_level = ? and uoc_subject = ? and uoc_course_filter = ?'
            # elif type_id == 5:
            #       # and
            #       # TODO hard! have to go look for hierarchy tables
            # elif type_id == 6:
            #       # or
            else:
                raise Exception(f'type_id {type_id} not recognized')

        elif table == 'CourseRequirementHierarchies':
            check = 'SELECT parent_id, child_id FROM CourseRequirementHierarchies where parent_id = ? and child_id = ?'
        elif table == 'DegreeOfferingRequirements':
            check = 'SELECT offering_degree_id, offering_year_id, requirement_id, uoc_needed, alt_text, id FROM DegreeOfferingRequirements WHERE offering_degree_id = ? and offering_year_id = ? and requirement_id = ? and uoc_needed = ? and alt_text = ?'
        elif table == 'DegreeOfferingNotes':
            check = 'SELECT offering_degree_id, offering_year_id, note, id FROM DegreeOfferingNotes WHERE offering_degree_id = ? and offering_year_id = ? and note = ?'
        elif table == 'CourseOfferings':
            check = 'SELECT course_id, session_year, session_term FROM CourseOfferings WHERE course_id = ? and session_year = ? and session_term = ?'
        elif table == 'CourseRequirementTypes':
            check = 'SELECT name, id from CourseRequirementTypes WHERE name = ?'
        elif table == 'CourseFilterTypes':
            check = 'SELECT name, id FROM CourseFilterTypes WHERE name = ?'
        else:
            raise Exception(f'Parsed table name {table} invalid')

        exists, item_id = self.has_entry(check, values)

        return exists, item_id


    def insert(self, msg, values):
        '''
        Inserts using the given <msg> string with ? placeholders
        And passes in <values>, the tuple of values for execute
        Returns the id of this inserted item (using auto-increment)

        Call self.check_exists() first. This function assumes entry DNE.
        Or use self.safe_insert()

        Assuming <msg> starts with 'INSERT INTO table_name(...)', 
        first parentheses is optional.
        '''
        self.cursor.execute(msg, values)
        self.db.commit()

        return self.cursor.lastrowid

    def courses_equivalent_add(self, first_course, second_course):
        '''
        Adds an EquivalentCourses relation between the two courses
        '''
        first_course_id = self.get_course_id(first_course)
        second_course_id = self.get_course_id(second_course)

        if second_course_id < first_course_id:
            # ids must be in ascending order
            first_course_id, second_course_id = second_course_id, first_course_id

        self.cursor.execute('''insert or ignore into EquivalentCourses(first_course, second_course)
            values(?, ?)''', (first_course_id, second_course_id))
        self.db.commit()

    def courses_exclusion_add(self, first_course, second_course):
        '''
        Adds an EquivalentCourses relation between the two courses
        '''
        first_course_id = self.get_course_id(first_course)
        second_course_id = self.get_course_id(second_course)

        if second_course_id < first_course_id:
            # ids must be in ascending order
            first_course_id, second_course_id = second_course_id, first_course_id

        self.cursor.execute('''insert or ignore into ExcludedCourses(first_course, second_course)
            values(?, ?)''', (first_course_id, second_course_id))
        self.db.commit()

    def courses_req_add(self, course, field, course_req_id):
        '''
        Adds the CourseRequirements id <course_req_id> as a foreign key
        for the Course entry with code <course> (i.e. 'COMP1511')
        to the given <field> in ['pre', 'co'] for
        prerequisite, corequisten

        Get <course_req_id> from self.add_course_req
        '''

        course_id = self.get_course_id(course)

        # validate field
        field_options = ['pre', 'co']
        if field not in field_options:
            raise Exception(f'field {field} must be in {field_options}')

        # start update message
        msg = 'UPDATE Courses SET '

        if field == field_options[0]:
            # prerequisite
            msg += 'prereq'
        elif field == field_options[1]:
            # corequisite
            msg += 'coreq'

        msg += ' = ?, finished = 1 WHERE id = ?'

        # execute query here
        self.cursor.execute(msg, (course_req_id, course_id))
        self.db.commit()

    def combine_course_req(self, combo_type, reqs):
        '''
        Combines the ids of CourseRequirements in <reqs>
        into an aggregate CourseRequirement ('AndRequirement' or 'OrRequirement')

        <combo_type> = ['and', 'or']
        <reqs> = list of ids of CourseRequirements
        '''
        COMBO_ID_START = 5

        valid_combos = ['and', 'or']
        if combo_type not in valid_combos:
            raise Exception(f'combo type {combo_type} must be a combo CourseRequirementType: {valid_combos}')

        combo_id = COMBO_ID_START + valid_combos.index(combo_type)

        # make a CourseRequirement for this combo type
        msg = 'INSERT INTO CourseRequirements(type_id) VALUES (?)'

        # TODO not safe inserting this yet because logic is complicated
        last_id = self.insert(msg, (combo_id,))

        # for each requirement id, add it to CourseFilterHierarchies table
        msg = 'INSERT INTO CourseRequirementHierarchies(parent_id, child_id) VALUES (?, ?)'
        for r in reqs:
            self.safe_insert(msg, (last_id, r), (last_id, r))

        return last_id

    def make_course_req(self, ty, min_mark=None, course=None, degree_id=None,
        year=None, uoc_amount_required=None, uoc_min_level=None, uoc_subject=None, 
        uoc_course_filter=None):
        '''
        Add an entry to CourseRequirements. Base types only.
        <ty> in ['completed', 'current', 'year', 'uoc', parsed into type_id
        <course> like 'COMP1511'

        If the type_id is a composite type, also adds the aggregated entries

        Returns the id of the inserted item
        '''

        # figure out what type of requirement
        valid_types = ['completed', 'current', 'year', 'uoc']
        if ty not in valid_types:
            raise Exception(f'type {ty} must be a base CourseRequirementTypes: {valid_types}')
        type_id = valid_types.index(ty) + 1     # ids start from 1 not 0

        if ty == 'completed':
            msg = 'INSERT INTO CourseRequirements(type_id, min_mark, course_id) VALUES (?, ?, ?)'
            course_id = self.get_course_id(course)
            # no min mark specified, assume you just need to pass
            if min_mark is None:
                min_mark = 50
            val_tuple = (type_id, min_mark, course_id)
            last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
        elif ty == 'current':
            msg = 'INSERT INTO CourseRequirements(type_id, degree_id) VALUES (?, ?)'
            val_tuple = (type_id, degree_id)
            last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
        elif ty == 'year':
            msg = 'INSERT INTO CourseRequirements(type_id, year) VALUES (?, ?)'
            val_tuple = (type_id, year)
            last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
        elif ty == 'uoc':
            msg = '''INSERT INTO CourseRequirements(type_id, uoc_amount_required, uoc_min_level, 
                uoc_subject, uoc_course_filter) VALUES (?, ?, ?, ?, ?)'''
            val_tuple = (type_id, uoc_amount_required, uoc_min_level, uoc_subject, uoc_course_filter)
            last = self.safe_insert(msg, val_tuple, val_tuple, type_id)

        return last

    def add_sessions(self, start, end):
        '''
        Adds sessions for the uni from start year to end year
        for all terms 0-3 (summer to T3)
        '''
        for year in range(start, end + 1):
            for term in range(3 + 1):
                msg = 'INSERT INTO Sessions(year, term) VALUES (?, ?)'
                vals = (year, term)
                self.safe_insert(msg, vals, vals)

    def add_course_offerings(self, course, years, terms):
        '''
        Adds to CourseOfferings for the given <course> in 'COMP1511' format.
        <years> is a list of years the offerings should be added for, i.e. [2019, 2020, 2021]
        <terms> is a list of terms the course is offered per year, i.e. [0, 1] for summer and T1
        - assuming that terms are the same every year. If different make 2 calls to function
        '''
        course_id = self.get_course_id(course)

        for y in years:
            for t in terms:
                msg = '''INSERT INTO CourseOfferings(course_id, session_year, session_term)
                    VALUES (?, ?, ?)'''
                vals = (course_id, y, t)
                self.safe_insert(msg, vals, vals)

    def combine_course_filters(self, combo_type, reqs):
        '''
        Combines the ids of CourseFilters entries in list reqs
        into an aggregate CourseFilters 'AndFilter' or 'OrFilter'

        Returns id of inserted CourseFilters entry
        '''
        COMBO_ID_START = 6
        valid_combos = ['and', 'or']
        if combo_type not in valid_combos:
            raise Exception(f'combo type {combo_type} must be a combo CourseFilterTypes: {valid_combos}')
        combo_id = COMBO_ID_START + valid_combos.index(combo_type)

        # make a CourseFilters for this combo type
        msg = 'INSERT INTO CourseFilters(type_id) VALUES (?)'
        last_id = self.insert(msg, (combo_id,))

        # for each requirement id, add it to the CourseFilterHierarchies table
        msg = 'INSERT INTO CourseFilterHierarchies(parent_id, child_id) VALUES (?, ?)'
        for r in reqs:
            vals = (last_id, r)
            self.safe_insert(msg, vals, vals)

        return last_id


    def add_course_filter(self, ty, min_mark=None, course=None,
        field_code=None, level=None, id=None):
        '''
        Inserts an entry into CourseFilters table
        <ty> is the type of CourseFilters entry, must be in <valid_types> list
        <course> is a string like 'COMP1511' which will be converted to course id

        Returns id of inserted CourseFilters entry
        '''
        valid_types = ['spec', 'gen', 'field', 'level', 'free']
        if ty not in valid_types:
            raise Exception(f'type {ty} must be a base CourseFilter: {valid_types}')
        type_id = valid_types.index(ty) + 1

        inserted_id = None

        msg = 'INSERT INTO CourseFilters(type_id'
        if ty == 'spec':
            msg += ', min_mark, course_id) VALUES (?, ?, ?)'
            course_id = self.get_course_id(course)
            vals = (type_id, min_mark, course_id)
        elif ty == 'field':
            msg += ', field_code) VALUES (?, ?)'
            vals = (type_id, field_code)
        elif ty == 'level':
            msg += ', level) VALUES (?, ?)'
            vals = (type_id, level)
        elif ty == 'gen' or ty == 'free':
            msg += ') VALUES (?)'
            vals = (type_id,)

        inserted_id = self.safe_insert(msg, vals, vals, type_id)

        return inserted_id

    def spec_courses_to_filters(self, course_names, min_mark=50):
        '''
        Inserts the list of specific course names in `course_names` as
        course filters with the given `min_mark`.

        Returns a list of the corresponding course filters
        '''
        filters = []
        for course in course_names:
            filters.append(self.add_course_filter('spec', min_mark=min_mark, course=course))

        return filters

    def add_degree_reqs(self, degree_code, year, filter_id, uoc_needed, alt_text=None):
        '''
        Inserts entry to DegreeOfferingRequirements table
        <degree_code> is an id of Degrees table
        <year> is a year that degree is offered, (<year>, <degree_code>) is entry in DegreeOfferings
        <filter_id> is the id of a CourseFilters entry describing a requirement for this DegreeOffering
        <uoc_needed> is the associated UOC needed for this requirement
        '''

        # get DegreeOffering id from degree_code, year
        exists, offer_id = self.check_exists('DegreeOfferings', (year, degree_code))

        if not exists:
            raise Exception(f'DegreeOffering for year = {year} and degree_id = {degree_code} DNE')

        msg = '''INSERT INTO DegreeOfferingRequirements(offering_degree_id, offering_year_id, requirement_id, uoc_needed, alt_text)
            VALUES (?, ?, ?, ?, ?)'''
        vals = (degree_code, year, filter_id, uoc_needed, alt_text)
        inserted_id = self.safe_insert(msg, vals, vals)         

        return inserted_id

    def add_degree_notes(self, degree_code, year, note):
        '''
        Inserts the `note` into DegreeOfferingNotes
        '''

        msg = '''INSERT INTO DegreeOfferingNotes(offering_degree_id, offering_year_id, note)
            VALUES (?, ?, ?)'''
        vals = (degree_code, year, note)
        inserted_id = self.safe_insert(msg, vals, vals)

        return inserted_id

    def add_degree(self, name, faculty, duration, degree_code):
        '''
        Inserts an entry into Degrees
        '''
        msg = 'INSERT INTO Degrees(name, faculty, duration, id) VALUES (?, ?, ?, ?)'
        vals = (name, faculty, duration, degree_code)
        uniques = (degree_code,)
        inserted_id = self.safe_insert(msg, vals, uniques)

        return inserted_id

    def add_degree_offering(self, year, degree_id):

        exists, offer_id = self.check_exists('Degrees', (degree_id,))

        if not exists:
            raise Exception(f'Degrees doesn\'t contain id {degree_id}, so cannot insert DegreeOfferings')

        msg = 'INSERT INTO DegreeOfferings(year, degree_id) VALUES (?, ?)'
        vals = (year, degree_id)
        inserted_id = self.safe_insert(msg, vals, vals)

        return inserted_id


    def close(self):
        self.db.close()
