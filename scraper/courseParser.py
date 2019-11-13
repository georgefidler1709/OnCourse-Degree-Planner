# '''
# Parser for courses
# '''

# from typing import List, Tuple, Optional
# class CourseParser(object):

#     def __init__(self):
#         pass

#     # Parse the string to return the list of term offerings
#     def parse_terms(self) -> List['term.Term']:
#         terms: List['term.Term'] = []
#         for i in range(1, 4):
#             if str(i) in self.terms:
#                 terms.append(term.Term(self.year, i))
#         return terms
#         # TODO summer terms

#     # Split a str of bracketed phrases by the outer level conjunction
#     # Return: list of split phrases and the conjunction joining them
#     # Note: outer brackets of phrases removed
#     def split_by_conj(self, string: str) -> Tuple[List[str], Optional[str]]:
#         pass

#     # interpret a string containing a single course requirement
#     def make_single_course_req(self, string) -> 'courseReq.CourseReq':
#         split = string.split()
        
#         #POSSIBLY MOD SUBJREQ TO TAKE COURSE CODE RATHER THAN COURSE OBJECT??
#         if len(split) == 1:
#             c = load_course(split[0])
        
#         if course is not None:
#             return subjectReq.SubjectReq(c)
        
#         elif split[0].lower() == "wam":
#             return wamReq.WAMReq(split[1])
        
#         elif split[0].lower() == "year":
#             return yearReq.YearReq(split[1])
        
#         # CAN WE LOAD A FILTER FROM DB??
#         elif split[0].lower() == "uoc":
#             units = int(split[1])
#             if len(split) > 2:
#                 filter = parse_uoc_req_filter(split)
#                 return uocReq.UOCReq(units, filter)
#             return uocReq.UOCReq(units)

#         # HOW DO WE HANDLE DEGREE/FACULTY/ETC
#         elif split[0].lower() == "enrol":
#             pass

#     # parse a string containing a possibly nested course requirement
#     def parse_course_req(self, req_str: str) -> Optional['courseReq.CourseReq']:
#         # split by outer conjunctions
#         tokenised = split_by_conj(req_str)

#         # this was a single course req
#         if conj == None:
#             return make_single_course_req(tokenised[0])

#         reqs = []
#         for s in tokenised:
#             reqs.append(parse_course_req(s))

#         # something has gone wrong
#         # notify somehow? Catalogue for manual checking?
#         if len(reqs) == 0:
#             return None
        
#         # create the composite req
#         if conj.lower() == "and":
#             return andReq.AndReq(reqs)

#         elif conj.lower() == "or":
#             return orReq.OrReq(reqs)

#         return None

#     # Parse a string containing a course requirement
#     def parse_req(self, req: str) -> Optional['courseReq.CourseReq']:
#         if self.prereqs == None:
#             return None
        
#         if self.prereqs == "":
#             return None

#         return parse_course_req(req)

#     # could we store equivalents as strings?
#     # course == str where str == course code??
#     def parse_eq(self, codes: List[str]) -> List['course.Course']:
#         pass