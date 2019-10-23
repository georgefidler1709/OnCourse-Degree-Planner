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

	def insert(self, msg, values):
		'''
		Inserts using the given <msg> string with ? placeholders
		And passes in <values>, the tuple of values for execute
		Returns the id of this inserted item (using auto-increment)
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
		last_id = self.insert(msg, (combo_id))

		# for each requirement id, add it to CourseFilterHierarchies table
		msg = "INSERT INTO CourseFilterHierarchies(parent_id, child_id) VALUES (?, ?)"
		for r in reqs:
			self.insert(last_id, r)

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
			last = self.insert(msg, (type_id, min_mark, course_id))
		elif ty == "current":
			msg = "INSERT INTO CourseRequirements(type_id, degree_id) VALUES (?, ?)"
			last = self.insert(msg, (type_id, degree_id))
		elif ty == "year":
			msg = "INSERT INTO CourseRequirements(type_id, year) VALUES (?, ?)"
			last = self.insert(msg, (type_id, year))
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
	comp1511 = self.make_course_req("completed", course="COMP1511")
	seng1020 = self.make_course_req("completed", course="SENG1020")
	seng1031 = self.make_course_req("completed", course="SENG1031")
	seng1010 = self.make_course_req("completed", course="SENG1010")

	# COMP1511
	self.courses_req_add("COMP1511", "ex", dpst1091)

	# COMP1521
	comp1521_or = self.combine_course_req("or", [comp1511, dpst1091, comp1911, comp1917])
	self.courses_req_add("COMP1521", "pre", comp1521_or)
	self.courses_req_add("COMP1521", "ex", dpst1092)

	# COMP1531
	comp1531_or = self.combine_course_req("or", [comp1511, dpst1091, comp1917, comp1921])
	self.courses_req_add("COMP1531", "pre", comp1531_or)
	comp1531_ex = self.combine_course_req("and", [seng1020, seng1031, seng1010])
	self.courses_req_add("COMP1531", "ex", comp1531_ex)
	
	# COMP2511
	# TODO ELENI etc.

	# see "On Course Database" google sheet, page "Courses" for what other courses we need
	# then we also need degree requirements, etc. 



	h.close()

if __name__ == "__main__":
	pass
	# compsci_course_reqs()