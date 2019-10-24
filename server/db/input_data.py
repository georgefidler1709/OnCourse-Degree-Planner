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
		course_id = cursor.fetchone()[0]

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

		Call self.check_exists first. This function assumes entry DNE.

		Assuming <msg> starts with "INSERT INTO table_name(...)", 
		first parentheses is optional.
		'''
		# TODO ELENI check that the record doesn't already exist
		# if it does, then get the id instead of trying to insert another entry
		self.cursor.execute(msg, values)
		self.db.commit()

		return self.lastrowid

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
		# TODO we don't have "equivalent" courses, see COMP1511 page
		field_options = ["pre", "co", "ex"]
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
		else:
			# exclusion
			msg += "exclusion"

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
		COMBO_ID_START = 4

		valid_combos = ["and", "or"]
		if combo_type not in valid_combos:
			raise Exception(f"combo type {combo_type} must be a combo CourseRequirementType: {valid_combos}")

		combo_id = COMBO_ID_START + valid_combos.index(combo_type)

		# make a CourseREquirement for this combo type
		msg = "INSERT INTO CourseRequirements(type_id) VALUES (?)"

		# TODO not safe inserting this yet because logic is complicated
		last_id = self.insert(msg, (combo_id))

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
			last = self.safe_insert(msg, (type_id, min_mark, course_id), (type_id, min_mark, course_id), type_id)
		elif ty == "current":
			msg = "INSERT INTO CourseRequirements(type_id, degree_id) VALUES (?, ?)"
			last = self.safe_insert(msg, (type_id, degree_id), (type_id, degree_id), type_id)
		elif ty == "year":
			msg = "INSERT INTO CourseRequirements(type_id, year) VALUES (?, ?)"
			last = self.safe_insert(msg, (type_id, year), (type_id, year), type_id)
		elif ty == "uoc":
			# TODO given the non-none arguments, insert them
			raise Exception('Helper._uoc_req() not implemented yet!!')

		return last

	def close(self):
		self.db.close()


def compsci_course_reqs():
	'''
	Statements to insert CourseRequirements for Computer Science (3778) (COMPA1) courses
	i.e. MVP
	'''
	h = Helper()

	# completed course reqs you can reuse
	dpst1091 = self.make_course_req("completed", course="DPST1091")
	dpst1092 = self.make_course_req("completed", course="DPST1092")
	comp1911 = self.make_course_req("completed", course="COMP1911")
	comp1921 = self.make_course_req("completed", course="COMP1921")
	comp1917 = self.make_course_req("completed", course="COMP1917")
	comp1927 = self.make_course_req("completed", course="COMP1927")
	comp1511 = self.make_course_req("completed", course="COMP1511")
	comp2011 = self.make_course_req("completed", course="COMP2011")
	comp2521 = self.make_course_req("completed", course="COMP2521")
	comp2911 = self.make_course_req("completed", course="COMP2911")
	seng1020 = self.make_course_req("completed", course="SENG1020")
	seng1031 = self.make_course_req("completed", course="SENG1031")
	seng1010 = self.make_course_req("completed", course="SENG1010")

	# COMP1511
	self.courses_req_add("COMP1511", "ex", dpst1091)
	print("... COMP1511")

	# COMP1521
	comp1521_or = self.combine_course_req("or", [comp1511, dpst1091, comp1911, comp1917])
	self.courses_req_add("COMP1521", "pre", comp1521_or)
	self.courses_req_add("COMP1521", "ex", dpst1092)
	print("... COMP1521")

	# COMP1531
	comp1531_or = self.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
	self.courses_req_add("COMP1531", "pre", comp1531_or)
	comp1531_ex = self.combine_course_req("and", [seng1020, seng1031, seng1010])
	self.courses_req_add("COMP1531", "ex", comp1531_ex)
	print("... COMP1531")
	type_id

	# COMP2511
	comp2511_small_or = self.combine_course_req("or", [comp2521, comp1927])
	comp2511_and = self.combine_course_req("and", [comp1531, comp2511_small_or])
	self.courses_req_add("COMP2511", "pre", comp2511_and)
	comp2511_ex = self.combine_course_req("and", [comp2911, comp2011])
	self.courses_req_add("COMP2511", "ex", comp2511_ex)

	# TODO ELENI etc.

	# see "On Course Database" google sheet, page "Courses" for what other courses we need
	# then we also need degree requirements, etc. 



	h.close()

if __name__ == "__main__":
	pass
	# compsci_course_reqs()