'''
Class to try and make populating the database
less painful.
'''
import sqlite3

class Helper:

	def __init__(self, dbaddr='university.db'):
		self.db = sqlite3.connect(dbaddr)
		self.cursor = self.db.cursor()

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
			if 'id' in results[0]:
				item_id = results[0]['id']
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
			check = "SELECT min_mark, course_id, id FROM CourseFilters where min_mark = ? and course_id = ?"
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

	def close(self):
		self.db.close()


def compsci_course_reqs(db="university.db"):
	'''
	Statements to insert CourseRequirements for Computer Science (3778) (COMPA1) courses
	i.e. MVP
	'''
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

if __name__ == "__main__":
	# pass
	compsci_course_reqs()