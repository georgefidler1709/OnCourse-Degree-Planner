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
        self.prereq_words = ['prereq:', 'prerequisite:', 'pre-requisite:']
        self.coreq_words = ['coreq:', 'corequisite:', 'co-requisite', 'prerequisite/corequisite:']
        self.and_words = [', and ', '; and ', ', including', ' including ', ', plus ', ' plus ', '+', ', ']
        self.or_words = [', or ', '; or ', '/']
        self.uoc_words = [' units of credit ', ' units ', ' units credit ', ' credits ']
        self.level_words = [' level ']
        self.ignore_words = [' at ', ' in ', ' overall ']

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
    def split_by_conj(self, string: str) -> Tuple[List[str], Optional[str], bool]:
        # find outer level conjunctions
        break_points: List[int] = []
        bracket_depth = 0
        conj = None
        length = len(string)

        for i in range(0, length):
            if string[i] == '(':
                bracket_depth += 1
            elif string[i] == ')':
                if bracket_depth > 0:
                    bracket_depth -= 1
                else:
                    # Error, inconsistent bracketing
                    print('INCONSISTENT BRACKETING')
                    return ([string], None, False)

            elif bracket_depth > 0:
                # Don't need to bother checking if it's an and, because it will be inside brackets
                continue
            elif string[i] == ' ':
                if string.find(' and ', i) == i:
                    # This has ANDs on the outside
                    if conj is None:
                        conj = 'and'
                    elif conj != 'and':
                        # Already have ORs, so this is an error
                        print('MIX AND WITH OR')
                        return ([string], None, False)
                        
                    break_points.append(i)
                elif string.find(' or ', i) == i:
                    # This has ORs on the outside
                    if conj is None:
                        conj = 'or'
                    elif conj != 'or':
                        # Already have ANDs, so this is an error
                        print('MIX OR WITH AND')
                        return ([string], None, False)

                    break_points.append(i)

        #should now have list of breakpoints corresponding to closing brackets

        # remove outer level brackets in the situation where the whole thing is in one set of
        # brackets
        if len(break_points) == 0 and string[0] == '(' and string[-1] == ')':
            string = string[1:-1]
            return ([string], '()', True)

        # no brackets = split on conjunctions
        if len(break_points) == 0:
            # split string
            if string.find(' or ') > 0:
                return (string.split(' or '), 'or', True)
            elif string.find(' and ') > 0:
                return (string.split(' and '), 'and', True)
            else:
                return ([string], None, True)

        # bracketed subphrases to consider
        if conj is None:
            # Error, if we have any subphrases then there should be a conj
            print('SUBPHRASES WITH NO CONJ')
            return ([string], None, False)
        strs: List[str] = []

        start = 0
        for end in break_points:
            split_string = string[start:end]
            split_string.strip()
            strs.append(split_string)
            start = end + len(conj) + 2

        final_part = string[start:]
        final_part.strip()
        strs.append(final_part)


        return (strs, conj, True)


    # Parse standard form of uoc req filter spec and return appropriate filter
    def parse_uoc_req_filter(self, req: List[str]) -> Optional['courseFilter.CourseFilter']:
        fields: List[str] = []
        levels: List[int] = []
        f: bool = False
        l: bool = False
        for word in req[2:]:
            if word == 'f':
                f = True
                l = False
            elif word == 'l':
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
                course, mark = split
                if mark.isdigit():
                    return scrapedSubjectReq.ScrapedSubjectReq(course, int(mark))

        # WAM requirements
        elif 'wam' in split:
            if split[0] == 'wam' and split[1].isdigit() and len(split) == 2:
                return wamReq.WAMReq(int(split[1]))
            elif split[1] == 'wam' and split[0].isdigit() and len(split) == 2:
                return wamReq.WAMReq(int(split[0]))
            else:
                print('COULD NOT PARSE WAM REQ')
                return None

        # year requirements
        elif split[0] == 'year' and len(split) == 2:
            return yearReq.YearReq(int(split[1]))

        # UOC requirements
        elif 'uoc' in split:
            print(split)
            if split[0] == 'uoc' and split[1].isdigit() and int(split[1]) % 6 == 0:
                units = int(split[1])
            elif split[1] == 'uoc' and split[0].isdigit() and int(split[0]) % 6 == 0:
                units = int(split[0])
            else:
                # could not parse req
                print('COULD NOT PARSE UOC REQ')
                return None

            if len(split) > 2:
                filter = self.parse_uoc_req_filter(split)
                if filter is None:
                    # could not parse filter
                    print('COULD NOT PARSE COURSE FILTER')
                    return None
                else:
                    return uocReq.UOCReq(units, filter)
            else:
                return uocReq.UOCReq(units)

        # enrollment requirements
        elif split[0] == 'enrol' and len(split) == 2:

            degree = int(split[1])
            return scrapedEnrollmentReq.ScrapedEnrollmentReq(degree)

        # something has gone wrong
        print('ERROR: could not parse course req')
        print(string)
        return None

    # parse a string containing a possibly nested course requirement
    def parse_course_req(self, req_str: str) -> Optional['courseReq.CourseReq']:
        # strip trailing characters and whitespace
        req = self.strip_punct_whitespace(req_str)

        # split by outer conjunctions
        tokenised, conj, success = self.split_by_conj(req)

        # something went wrong in splitting
        if not success:
            return None

        # this was a single course req
        if conj == None:
            return self.make_single_course_req(tokenised[0])

        # The whole thing was in one set of brackets, start again without the brackets
        if conj == '()':
            return self.parse_course_req(tokenised[0])

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

    def strip_word(self, string: str, word: str) -> str:

        result = string.strip()
        result = string.strip(word)

        return result.strip()

    def strip_punct_whitespace(self, string: str) -> str:
        result = string.strip()
        result = result.strip('.')
        result = result.strip(';')
        result = result.strip()
        return result

    def replace_prereq_coreq(self, string: str) -> str:
        for word in self.prereq_words:
            string = string.replace(word, 'prereq')
        for word in self.coreq_words:
            string = string.replace(word, 'coreq')
        return string

    def replace_conj(self, string: str) -> str:
        for word in self.and_words:
            string = string.replace(word, ' and ')
        for word in self.or_words:
            string = string.replace(word, ' or ')
        return string

    def replace_keywords(self, string: str) -> str:
        for word in self.uoc_words:
            string = string.replace(word, ' uoc ')
        for word in self.level_words:
            string = string.replace(word, ' l ')
        return string

    def strip_ignore_words(self, string: str) -> str:
        for word in self.ignore_words:
            if string.find(word) >= 0:
                string = string.replace(word, ' ')
        return string

    # Parse a string containing a course requirement
    def parse_reqs(self, req: str) -> Tuple[Optional['courseReq.CourseReq'], Optional['courseReq.CourseReq'], bool]:
        status: bool=True
        if req == None:
            return (None, None, status)

        if req == '':
            return (None, None, status)

        # convert to lower case
        req = req.lower()
        req = self.strip_punct_whitespace(req)
        req = self.replace_prereq_coreq(req)
        req = self.replace_conj(req)
        req = self.replace_keywords(req)
        req = self.strip_ignore_words(req)

        co = req.find('coreq')
        pre = req.find('prereq')

        if pre < 0 and co >= 0:
            prereqs = None
            coreq_str = req[co:]
            coreq_str = self.strip_word(coreq_str, 'coreq')
            coreqs = self.parse_course_req(coreq_str)
            if not coreqs:
                status = False

        elif pre >= 0 and co < 0:
            coreqs = None
            prereq_str = req[pre:]
            prereq_str = self.strip_word(prereq_str, 'prereq')
            prereqs = self.parse_course_req(prereq_str)
            if not prereqs:
                status = False

        elif pre >= 0 and co >= 0:
            coreq_str = req[co:]
            coreq_str = self.strip_word(coreq_str, 'coreq')
            coreqs = self.parse_course_req(coreq_str)
            if not coreqs:
                status = False
            prereq_str = req[pre:co]
            prereq_str = self.strip_word(prereq_str, 'prereq')
            prereqs = self.parse_course_req(prereq_str)
            if not prereqs:
                status = False

        else:
            coreqs = None
            prereq_str = req
            prereq_str = prereq_str.strip()
            prereqs = self.parse_course_req(prereq_str)
            if not prereqs:
                status = False

        return (prereqs, coreqs, status)
