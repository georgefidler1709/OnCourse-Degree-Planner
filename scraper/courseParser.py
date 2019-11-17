'''
Parses course information
'''

from typing import List, Tuple, Optional

from classes import course
from classes import term
from classes import courseFilter
from classes import fieldFilter
from classes import levelFilter
from classes import orFilter
from classes import andFilter
from . import scrapedEnrollmentReq
from . import scrapedSubjectReq
from classes import courseReq
from classes import yearReq
from classes import uocReq
from classes import wamReq
from classes import andReq
from classes import orReq


class CourseParser(object):

    def __init__(self):
        pass

    # Parse the string to return the list of term offerings
    def parse_terms(self, string: str, year: int) -> List['term.Term']:
        terms: List['term.Term'] = []
        for i in range(1, 4):
            if str(i) in string:
                terms.append(term.Term(year, i))
        return terms
    # TODO summer terms

    def is_course_code(self, string: str) -> bool:
        if string[:4].isalpha() and string[4:].isdigit():
            return True
        return False

    # Split a str of bracketed phrases by the outer level conjunction
    # Return: list of split phrases and the conjunction joining them
    # Note: outer brackets of phrases removed
    def split_by_conj(self, string: str) -> Tuple[List[str], Optional[str]]:
        # find outer level conjunctions
        break_points: List[int] = []
        brackets: List[str] = []

        length = len(string)
        for i in range(0, length):
            if string[i] == '(':
                brackets.append(string[i])
            elif string[i] == ')':
                if len(brackets) == 1:
                    if i < length - 3:
                        if string[i+2].lower() == 'a':
                            conj = 'and'
                        elif string[i+2].lower() == 'o':
                            conj = 'or'
                        else:
                            print("ERROR splitting requirements for course:")
                            print(string)
                            # For now set the conj to nothing, because of the error splitting
                            conj = ''
                    break_points.append(i+1)
                    brackets = []
                else:
                    brackets.pop()

        #should now have list of breakpoints corresponding to closing brackets

        # remove brackets around a single compositeReq
        if len(break_points) == 1:
            string = string[1:-1]

        # no brackets = split on conjunctions
        if len(break_points) < 2:
            if string.find(' or ') > 0:
                return (string.split(' or '), 'or')
            elif string.find(' and ') > 0:
                return (string.split(' and '), 'and')
            else:
                return ([string], None)

        # bracketed subphrases to consider
        strs: List[str] = []

        start = 0
        for end in break_points:
            split_string = string[start:end]
            split_string.strip()
            strs.append(split_string)
            start = end + len(conj) + 2

        return (strs, conj)


    # Parse standard form of uoc req filter spec and return appropriate filter
    def parse_uoc_req_filter(self, req: List[str]) -> Optional['courseFilter.CourseFilter']:
        fields: List[str] = []
        levels: List[int] = []
        f: bool = False
        l: bool = False
        for word in req[2:]:
            if word == "f":
                f = True
                l = False
            elif word == "l":
                f = False
                l = True
            elif f:
                fields.append(word)
            elif l:
                levels.append(int(word))

        field_filters: List['courseFilter.CourseFilter'] = []
        level_filters: List['courseFilter.CourseFilter'] = []

        for field in fields:
            field_filters.append(fieldFilter.FieldFilter(field))
        for level in levels:
            level_filters.append(levelFilter.LevelFilter(level))

        ffs = None
        lfs = None
        if len(field_filters) == 1:
            ffs = field_filters[0]
        elif len(field_filters) > 1:
            ffs = orFilter.OrFilter(field_filters)
        if len(level_filters) == 1:
            lfs = level_filters[0]
        if len(level_filters) > 1:
            lfs = orFilter.OrFilter(level_filters)

        if ffs and lfs:
            return andFilter.AndFilter([ffs, lfs])
        elif ffs:
            return ffs
        elif lfs:
            return lfs
        else:
            return None


    # interpret a string containing a single course requirement
    def make_single_course_req(self, string: str) -> Optional['courseReq.CourseReq']:
        split = string.split()

        # subject requirements
        if self.is_course_code(split[0]):
            if len(split) == 1:
                return scrapedSubjectReq.ScrapedSubjectReq(split[0])
            elif len(split) == 2:
                return scrapedSubjectReq.ScrapedSubjectReq(split[0], int(split[1]))

        # WAM requirements
        elif split[0].lower() == "wam":
            return wamReq.WAMReq(int(split[1]))

        # year requirements
        elif split[0].lower() == "year":
            return yearReq.YearReq(int(split[1]))

        # UOC requirements
        elif split[0].lower() == "uoc":
            units = int(split[1])
            if len(split) > 2:
                filter = self.parse_uoc_req_filter(split)
                return uocReq.UOCReq(units, filter)
            else:
                return uocReq.UOCReq(units)

        # enrollment requirements
        elif split[0].lower() == "enrol":
            degree = int(split[1])
            return scrapedEnrollmentReq.ScrapedEnrollmentReq(degree)

        # something has gone wrong
        print("ERROR: could not parse course req")
        print(string)
        return None

    # parse a string containing a possibly nested course requirement
    def parse_course_req(self, req_str: str) -> Optional['courseReq.CourseReq']:
        # split by outer conjunctions
        tokenised, conj = self.split_by_conj(req_str)

        # this was a single course req
        if conj == None:
            return self.make_single_course_req(tokenised[0])

        reqs = []
        for s in tokenised:
            r = self.parse_course_req(s)
            if r:
                reqs.append(r)
            else:
                return None

        if len(reqs) < 2:
            return None

        # create the composite req
        if conj == 'and':
            return andReq.AndReq(reqs)

        elif conj == 'or':
            return orReq.OrReq(reqs)

        return None

    def strip_word_and_whitespace(self, string: str, word: str) -> str:

        result = string.strip()
        result = string.strip(word)

        return result.strip()
        

    # Parse a string containing a course requirement
    def parse_reqs(self, req: str) -> Tuple[Optional['courseReq.CourseReq'], Optional['courseReq.CourseReq'], bool]:
        status: bool=True
        if req == None:
            return (None, None, status)

        if req == "":
            return (None, None, status)

        co = req.find('coreq')
        pre = req.find('prereq')

        if pre < 0:
            prereqs = None
        else:
            prereq_str = req[:co]
            prereq_str = self.strip_word_and_whitespace(prereq_str, 'prereq')
            prereqs = self.parse_course_req(prereq_str)
            if not prereqs:
                status = False

        if co < 0:
            coreqs = None
            prereqs = self.parse_course_req(req)
            if not prereqs:
                status = False
        else:
            coreq_str = req[co:]
            coreq_str = self.strip_word_and_whitespace(coreq_str, 'coreq')
            coreqs = self.parse_course_req(coreq_str)
            if not coreqs:
                status = False

        return (prereqs, coreqs, status)
