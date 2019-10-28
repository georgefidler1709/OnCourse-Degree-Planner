'''
Class to try and make populating the database
less painful.
'''
import sqlite3

class Helper:

	def __init__(self, dbaddr='university.db'):
		self.db = sqlite3.connect(dbaddr)
		self.cursor = self.db.cursor()
		self.cursor.row_factory = sqlite3.Row

	def get_course_id(self, course):
		'''
		<course> a string like "COMP1511"

		Returns the id of the Course entry corresponding to this course
		'''
		letter_code = course[:4]
		number_code = course[4:]

		# find the course id
		self.cursor.execute("SELECT id FROM Courses where letter_code = ? and number_code = ?",
			(letter_code, number_code))
		course_id = self.cursor.fetchone()[0]

		return course_id

	def has_entry(self, check_msg, values_tuple):
		'''
		Check if the given query returns results
		True if entry exists in db, otherwise False
		'''
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
		<msg> is the sql insert statement in form "INSERT INTO <table>(..."
		<values> is the tuple of values corresponding to ? in <msg>
		<unique_values> is a tuple of values needed to check this
		<table> is either "req", "filters", or None for types of tables with type_id arguments
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

		if table == "Degrees":
			check = "SELECT id FROM Degrees where id = ?"
		elif table == "DegreeOfferings":
			check = "SELECT year, degree_id FROM DegreeOfferings where year = ? and degree_id = ?"
		elif table == "Courses":
			check = "SELECT letter_code, number_code, id FROM courses where letter_code = ? and number_code = ?"
		elif table == "Sessions":
			check = "SELECT year, term FROM Sessions where year = ? and term = ?"
		elif table == "CourseFilters":

			if type_id is None:
				raise Exception("You need to specify a type_id for CourseFilters check")

			if type_id == 1:
				# specific course filter
				check = "SELECT type_id, min_mark, course_id, id FROM CourseFilters where type_id = ? and min_mark = ? and course_id = ?"
			elif type_id == 2:
				# gened filter
				check = "SELECT type_id, id FROM CourseFilters where type_id = ?"
			elif type_id == 3:
				# field filter
				check = "SELECT type_id, field_code, level, id FROM CourseFilters where type_id = ? and field_code = ? and level = ?"
			elif type_id == 4:
				# free elective filter
				check = "SELECT type_id, id FROM CourseFilters where type_id = ?"
			# TODO not checking AND or OR requirements yet cuz complicated

		elif table == "CourseFilterHierarchies":
			check = "SELECT parent_id, child_id from CourseFilterHierarchies where parent_id = ? and child_id = ?"
		elif table == "CourseRequirements":

			if type_id is None:
				raise Exception("You need to specify a type_id for CourseRequirements check")

			if type_id == 1:
				# completed
				check = "SELECT type_id, min_mark, course_id, id from CourseRequirements WHERE type_id = ? and min_mark = ? and course_id = ?"
			elif type_id == 2:
				# current degree
				check = "SELECT type_id, degree_id, id from CourseRequirements WHERE type_id = ? and degree_id = ?"
			elif type_id == 3:
				# year requirement
				check = "SELECT type_id, year, id from CourseRequirements WHERE type_id = ? and year = ?"
			elif type_id == 4:
				# UOC requirement
				check = "SELECT type_id, uoc_amount_required, uoc_min_level, uoc_subject, uoc_course_requirements, id FROM CourseRequirements WHERE type_id = ? and uoc_amount_required = ? and uoc_min_level = ? and uoc_subject = ? and uoc_course_requirements = ?"
			# elif type_id == 5:
			# 	# and
			# 	# TODO hard! have to go look for hierarchy tables
			# elif type_id == 6:
			# 	# or
			else:
				raise Exception(f"type_id {type_id} not recognized")

		elif table == "CourseRequirementHierarchies":
			check = "SELECT parent_id, child_id FROM CourseRequirementHierarchies where parent_id = ? and child_id = ?"
		elif table == "DegreeOfferingRequirements":
			check = "SELECT offering_id, requirement_id, uoc_needed, id FROM DegreeOfferingRequirements WHERE offering_id = ? and requirement_id = ? and uoc_needed = ?"
		elif table == "CourseOfferings":
			check = "SELECT course_id, session_year, session_term FROM CourseOfferings WHERE course_id = ? and session_year = ? and session_term = ?"
		elif table == "CourseRequirementTypes":
			check = "SELECT name, id from CourseRequirementTypes WHERE name = ?"
		elif table == "CourseFilterTypes":
			check = "SELECT name, id FROM CourseFilterTypes WHERE name = ?"
		else:
			raise Exception(f"Parsed table name {table} invalid")

		exists, item_id = self.has_entry(check, values)

		return exists, item_id


	def insert(self, msg, values):
		'''
		Inserts using the given <msg> string with ? placeholders
		And passes in <values>, the tuple of values for execute
		Returns the id of this inserted item (using auto-increment)

		Call self.check_exists() first. This function assumes entry DNE.
		Or use self.safe_insert()

		Assuming <msg> starts with "INSERT INTO table_name(...)", 
		first parentheses is optional.
		'''
		self.cursor.execute(msg, values)
		self.db.commit()

		return self.cursor.lastrowid

	def courses_req_add(self, course, field, course_req_id):
		'''
		Adds the CourseRequirements id <course_req_id> as a foreign key
		for the Course entry with code <course> (i.e. "COMP1511")
		to the given <field> in ["pre", "co", "ex"] for
		prerequisite, corequiste, exclusion

		Get <course_req_id> from self.add_course_req
		'''

		course_id = self.get_course_id(course)

		# validate field
		field_options = ["pre", "co", "ex", "eq"]
		if field not in field_options:
			raise Exception(f"field {field} must be in {field_options}")

		# start update message
		msg = "UPDATE Courses SET "

		if field == field_options[0]:
			# prerequisite
			msg += "prereq"
		elif field == field_options[1]:
			# corequisite
			msg += "coreq"
		elif field == field_options[2]:
			# exclusion
			msg += "exclusion"
		else:
			# equivalent
			msg += "equivalent"

		msg += " = ? WHERE id = ?"

		# execute query here
		self.cursor.execute(msg, (course_req_id, course_id))
		self.db.commit()

	def combine_course_req(self, combo_type, reqs):
		'''
		Combines the ids of CourseRequirements in <reqs>
		into an aggregate CourseRequirement ("AndRequirement" or "OrRequirement")

		<combo_type> = ["and", "or"]
		<reqs> = list of ids of CourseRequirements
		'''
		COMBO_ID_START = 5

		valid_combos = ["and", "or"]
		if combo_type not in valid_combos:
			raise Exception(f"combo type {combo_type} must be a combo CourseRequirementType: {valid_combos}")

		combo_id = COMBO_ID_START + valid_combos.index(combo_type)

		# make a CourseREquirement for this combo type
		msg = "INSERT INTO CourseRequirements(type_id) VALUES (?)"

		# TODO not safe inserting this yet because logic is complicated
		last_id = self.insert(msg, (combo_id,))

		# for each requirement id, add it to CourseFilterHierarchies table
		msg = "INSERT INTO CourseFilterHierarchies(parent_id, child_id) VALUES (?, ?)"
		for r in reqs:
			self.safe_insert(msg, (last_id, r), (last_id, r))

		return last_id

	def make_course_req(self, ty, min_mark=None, course=None, degree_id=None,
		year=None, uoc_amount_required=None, uoc_min_level=None, uoc_subject=None, 
		uoc_course_requirements=None):
		'''
		Add an entry to CourseRequirements. Base types only.
		<ty> in ["completed", "current", "year", "uoc", parsed into type_id
		<course> like "COMP1511"

		If the type_id is a composite type, also adds the aggregated entries

		Returns the id of the inserted item
		'''

		# figure out what type of requirement
		valid_types = ["completed", "current", "year", "uoc"]
		if ty not in valid_types:
			raise Exception(f"type {ty} must be a base CourseRequirementTypes: {valid_types}")
		type_id = valid_types.index(ty) + 1 	# ids start from 1 not 0

		if ty == "completed":
			msg = "INSERT INTO CourseRequirements(type_id, min_mark, course_id) VALUES (?, ?, ?)"
			course_id = self.get_course_id(course)
			# no min mark specified, assume you just need to pass
			if min_mark is None:
				min_mark = 50
			val_tuple = (type_id, min_mark, course_id)
			last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
		elif ty == "current":
			msg = "INSERT INTO CourseRequirements(type_id, degree_id) VALUES (?, ?)"
			val_tuple = (type_id, degree_id)
			last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
		elif ty == "year":
			msg = "INSERT INTO CourseRequirements(type_id, year) VALUES (?, ?)"
			val_tuple = (type_id, year)
			last = self.safe_insert(msg, val_tuple, val_tuple, type_id)
		elif ty == "uoc":
			msg = '''INSERT INTO CourseRequirements(type_id, uoc_amount_required, uoc_min_level, 
				uoc_subject, uoc_course_requirements) VALUES (?, ?, ?, ?, ?)'''
			val_tuple = (type_id, uoc_amount_required, uoc_min_level, uoc_subject, uoc_course_requirements)
			last = self.safe_insert(msg, val_tuple, val_tuple, type_id)

		return last

	def add_sessions(self, start, end):
		'''
		Adds sessions for the uni from start year to end year
		for all terms 0-3 (summer to T3)
		'''
		for year in range(start, end + 1):
			for term in range(3 + 1):
				msg = "INSERT INTO Sessions(year, term) VALUES (?, ?)"
				vals = (year, term)
				self.safe_insert(msg, vals, vals)

	def add_course_offerings(self, course, years, terms):
		'''
		Adds to CourseOfferings for the given <course> in "COMP1511" format.
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
		into an aggregate CourseFilters "AndFilter" or "OrFilter"

		Returns id of inserted CourseFilters entry
		'''
		COMBO_ID_START = 5
		valid_combos = ["and", "or"]
		if combo_type not in valid_combos:
			raise Exception(f"combo type {combo_type} must be a combo CourseFilterTypes: {valid_combos}")
		combo_id = COMBO_ID_START + valid_combos.index(combo_type)

		# make a CourseFilters for this combo type
		msg = "INSERT INTO CourseFilters(type_id) VALUES (?)"
		last_id = self.insert(msg, (combo_id,))

		# for each requirement id, add it to the CourseFilterHierarchies table
		msg = "INSERT INTO CourseFilterHierarchies(parent_id, child_id) VALUES (?, ?)"
		for r in reqs:
			vals = (last_id, r)
			self.safe_insert(msg, vals, vals)

		return last_id


	def add_course_filter(self, ty, min_mark=None, course=None,
		field_code=None, level=None, id=None):
		'''
		Inserts an entry into CourseFilters table
		<ty> is the type of CourseFilters entry, must be in <valid_types> list
		<course> is a string like "COMP1511" which will be converted to course id

		Returns id of inserted CourseFilters entry
		'''
		valid_types = ["spec", "gen", "field", "free"]
		if ty not in valid_types:
			raise Exception(f"type {ty} must be a base CourseFilter: {valid_types}")
		type_id = valid_types.index(ty) + 1

		inserted_id = None

		msg = "INSERT INTO CourseFilters(type_id"
		if ty == "spec":
			msg += ", min_mark, course_id) VALUES (?, ?, ?)"
			course_id = self.get_course_id(course)
			vals = (type_id, min_mark, course_id)
		elif ty == "field":
			msg += ", field_code, level) VALUES (?, ?, ?)"
			vals = (type_id, field_code, level)
		elif ty == "gen" or ty == "free":
			msg += ") VALUES (?)"
			vals = (type_id,)

		inserted_id = self.safe_insert(msg, vals, vals, type_id)

		return inserted_id

	def add_degree_reqs(self, degree_code, year, filter_id, uoc_needed):
		'''
		Inserts entry to DegreeOfferingRequirements table
		<degree_code> is an id of Degrees table
		<year> is a year that degree is offered, (<year>, <degree_code>) is entry in DegreeOfferings
		<filter_id> is the id of a CourseFilters entry describing a requirement for this DegreeOffering
		<uoc_needed> is the associated UOC needed for this requirement
		'''

		# get DegreeOffering id from degree_code, year
		exists, offer_id = self.check_exists("DegreeOfferings", (year, degree_code))

		if not exists:
			raise Exception(f"DegreeOffering for year = {year} and degree_id = {degree_code} DNE")

		msg = '''INSERT INTO DegreeOfferingRequirements(offering_id, requirement_id, uoc_needed)
			VALUES (?, ?, ?)'''
		vals = (offer_id, filter_id, uoc_needed)
		inserted_id = self.safe_insert(msg, vals, vals)

		return inserted_id

	def close(self):
		self.db.close()


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
	# finalyear = h.make_course_req("year", )

	# COMP1511
	h.courses_req_add("COMP1511", "ex", dpst1091)
	print("... COMP1511")

	# COMP1521
	comp1521_or = h.combine_course_req("or", [comp1511, dpst1091, comp1911, comp1917])
	h.courses_req_add("COMP1521", "pre", comp1521_or)
	h.courses_req_add("COMP1521", "ex", dpst1092)
	print("... COMP1521")

	# COMP1531
	comp1531_or = h.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
	h.courses_req_add("COMP1531", "pre", comp1531_or)
	comp1531_ex = h.combine_course_req("and", [seng1020, seng1031, seng1010])
	h.courses_req_add("COMP1531", "ex", comp1531_ex)
	print("... COMP1531")

	# COMP2511
	comp2511_small_or = h.combine_course_req("or", [comp2521, comp1927])
	comp2511_and = h.combine_course_req("and", [comp1531, comp2511_small_or])
	h.courses_req_add("COMP2511", "pre", comp2511_and)
	comp2511_ex = h.combine_course_req("and", [comp2911, comp2011])
	h.courses_req_add("COMP2511", "ex", comp2511_ex)
	print("... COMP2511")

	# TODO ELENI etc.

	# COMP2521
	# Prerequisite: COMP1511 or DPST1091 or COMP1917 or COMP1921
	comp2521_or = h.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
	h.courses_req_add("COMP2521", "pre", comp2521_or)
	h.courses_req_add("COMP2521", "ex", comp1927)
	print("... COMP2521")


	# COMP3900
	# Prerequisite: COMP1531, and COMP2521 or COMP1927,
	# and enrolled in a BSc Computer Science major with completion of 102 uoc.
	comp3900_or = h.combine_course_req("or", [comp2521, comp1927])
	comp3900_uoc = h.make_course_req("uoc", uoc_amount_required=102)
	comp3900_and = h.combine_course_req("and", [comp3900_or, compenrol, comp3900_uoc])
	h.courses_req_add("COMP3900", "pre", comp3900_and)
	comp3900_ex = h.combine_course_req("and", [comp9596, comp9945, comp9900])
	h.courses_req_add("COMP3900", "ex", comp3900_ex)
	print("... COMP3900")

	# COMP4920
	# Prerequisite: COMP2511 or COMP2911, and in the final year of the BSc Computer Science
	# or BE / BE (Hons) Bioinformatics Engineering or Computer Engineering.
	# Software Engineering students enrol in SENG4920.
	comp4920_or = h.combine_course_req("or", [comp2511, comp2911])
	comp4920_and = h.combine_course_req("and", [comp4920_or, compenrol])
	h.courses_req_add("COMP4920", "pre", comp4920_and)
	comp4920_ex = h.combine_course_req("and", [binf4920, seng4920, seng4921, comp2920])
	h.courses_req_add("COMP4920", "ex", comp4920_ex)
	print("... COMP4920")
	
	# MATH1081
	# Corequisite: MATH1131 or DPST1013 or MATH1141 or MATH1151
	math1081_or = h.combine_course_req("or", [math1131, dpst1013, math1141, math1151])
	h.courses_req_add("MATH1081", "co", math1081_or)
	h.courses_req_add("MATH1081", "ex", math1090)
	print("... MATH1081")

	# MATH1131
	# no prereqs
	h.courses_req_add("MATH1131", "eq", dpst1013)
	math1131_ex = h.combine_course_req("and", [dpst1013, math1151, math1031, math1141, econ2291, math1011, econ1202])
	h.courses_req_add("MATH1131", "ex", math1131_ex)
	print("... MATH1131")
	
	# MATH1141
	math1141_ex = h.combine_course_req("and", [dpst1013, math1151, math1031, math1131, econ2291, math1011, econ1202])
	h.courses_req_add("MATH1141", "ex", math1141_ex)
	print("... MATH1141")

	# MATH1231
	# Prerequisite: MATH1131 or DPST1013 or MATH1141
	math1231_or = h.combine_course_req("or", [math1131, dpst1013, math1141])
	h.courses_req_add("MATH1231", "pre", math1231_or)
	h.courses_req_add("MATH1231", "eq", dpst1014)
	math1231_ex = h.combine_course_req("and", [dpst1014, math1251, math1021, math1241])
	h.courses_req_add("MATH1231", "ex", math1231_ex)
	print("... MATH1231")

	# MATH1241
	# Prerequisite: MATH1131 (CR) or MATH1141 (CR) or DPST1013 (CR)
	math1241_or = h.combine_course_req("or", [math1131_cr, math1141_cr, dpst1013_cr])
	h.courses_req_add("MATH1241", "pre", math1241_or)
	math1241_ex = h.combine_course_req("and", [dpst1014, math1251, math1021, math1231])
	h.courses_req_add("MATH1241", "ex", math1241_ex)
	print("... MATH1241")

	# COMP3121
	# Prerequisite: COMP1927 or COMP2521
	comp3121_or = h.combine_course_req("or", [comp1927, comp2521])
	h.courses_req_add("COMP3121", "pre", comp3121_or)
	comp3121_eq = h.combine_course_req("and", [comp3821, comp9801, comp3120, comp9101])
	h.courses_req_add("COMP3121", "eq", comp3121_eq)
	print("... COMP3121")

	# COMP3821
	# Prerequisite: A mark of at least 65 in COMP1927 or COMP2521
	comp3821_or = h.combine_course_req("or", [comp1927_cr, comp2521_cr])
	h.courses_req_add("COMP3821", "pre", comp3821_or)
	comp3821_eq = h.combine_course_req("and", [comp3121, comp9801])
	h.courses_req_add("COMP3821", "eq", comp3821_eq)
	print("... COMP3821")
	


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

def insert_compsci_degree_requirements(db='university.db'):
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
	core_filters = []
	for course in core_courses:
		core_filters.append(h.add_course_filter("spec", min_mark=50, course=course))

	core_combo = h.combine_course_filters("and", core_filters)

	math1_filters = []
	for course in math1_opts:
		math1_filters.append(h.add_course_filter("spec", min_mark=50, course=course))
	math1_or = h.combine_course_filters("or", math1_filters)

	math2_filters = []
	for course in math2_opts:
		math2_filters.append(h.add_course_filter("spec", min_mark=50, course=course))
	math2_or = h.combine_course_filters("or", math2_filters)

	algos_filters = []
	for course in algos_opts:
		algos_filters.append(h.add_course_filter("spec", min_mark=50, course=course))
	algos_or = h.combine_course_filters("or", algos_filters)

	# comp elective filters, 30 UOC level 3, 4, 6, 9
	# "I guess you'd have OR(AND(COMP, level 3), AND(COMP, level4)) etc" - Eleni
	# WARNING making levels a part of filter that can be None / NULL if you just need any COMP course
	comp3 = h.add_course_filter("field", field_code="COMP", level=3)
	comp4 = h.add_course_filter("field", field_code="COMP", level=4)
	comp6 = h.add_course_filter("field", field_code="COMP", level=6)
	comp9 = h.add_course_filter("field", field_code="COMP", level=9)
	comp_elec = h.combine_course_filters("or", [comp3, comp4, comp6, comp9])

	# gen ed filters, 12 UOC
	gen_filter = h.add_course_filter("gen")

	# free elective filters, 36 UOC
	free_filter = h.add_course_filter("free")

	# ====== insert degree requirements =====
	print("===> Inserting Degree Requirements for COMPA1 Degree")
	COURSE_UOC = 6
	COMPSCI = 3778

	# core stuff
	h.add_degree_reqs(COMPSCI, 2019, core_combo, len(core_courses) * COURSE_UOC)
	h.add_degree_reqs(COMPSCI, 2019, math1_or, COURSE_UOC)
	h.add_degree_reqs(COMPSCI, 2019, math2_or, COURSE_UOC)
	h.add_degree_reqs(COMPSCI, 2019, algos_or, COURSE_UOC)

	# 30 UOC comp electives
	h.add_degree_reqs(COMPSCI, 2019, comp_elec, 30)
	
	# 12 UOC gen eds
	h.add_degree_reqs(COMPSCI, 2019, gen_filter, 12)

	# 36 UOC free electives
	h.add_degree_reqs(COMPSCI, 2019, free_filter, 36)

	h.close()




if __name__ == "__main__":
	
	# Computer Science (3778) (COMPA1) courses
	# compsci_course_reqs()
	# insert_sessions()
	# insert_course_offerings()
	insert_compsci_degree_requirements()

	pass