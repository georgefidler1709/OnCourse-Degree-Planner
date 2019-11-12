'''
Parser for course requirements
'''

class CourseReqLoader(object):

   def __init__(self):
       self.helper = Helper()

   def add_course(self, course_code, reqs):
       course_req = parse(reqs)

       # add course to db with reqs



   def parse(self, reqs: str) -> CourseReq:
        split string by prereq/coreq and trim

        if no CNJ in NP
        create course requirement and return

        else
        split by CNJ at top level
        type 'and' or 'or'

        for each NP separated by CNJ
        call parse recursively
        add coursereq to list

        create CNJ coursereq
        self.helper.combine_course_req()
        return


   def course_requirement_from_str(self, req: str) -> CourseReq:
       # determine what type of requirement
       if completion(req):
           helper.make_course_req("completed", )
       else if current(req)
       else if year(req)
       else if uoc(req)

       # else [ADD MANUALLY]
       # create requirement standard format
       # self.helper.make_course_req()
       # return requirement id

   def corequisite(self, req: str) -> bool:
       # if str contains? begins with?
       #["Coreq", "Coreqs" "Corequisite", "Corequisites"]
       pass

   # returns whether string corresponds to course completion requirement
   def completion(self, req: str) -> bool:
       # course code
       # mark?
       pass

   def current(self, req: str) -> bool:
       pass

   def year(self, req: str) -> bool:
       pass

   def uoc(self, req: str) -> bool:
       pass

