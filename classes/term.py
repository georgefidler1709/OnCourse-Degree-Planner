"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

term.py
A term study period consisting of a year and a term 1-3 or summer term.

[MORE INFO ABOUT CLASS]
"""

class Term(object):

    # define a new Term object
    # preconditions: (1 <= term <= 3)
    def __init__(self, year: int, term: int):
        self._year = year
        self._term = term

    @property
    def year(self):
        return self._year

    @property
    def term(self):
        return self._term

    # Override comparison functions
    def __lt__(self, other) -> bool: # x < y
        if self._year < other.year: return True
        if self._year > other.year: return False
        if self._term < other.term: return True
        return False
    
    def __le__(self, other) -> bool: # For x <= y
        if self._year < other.year: return True
        if self._year > other.year: return False
        if self._term <= other.term: return True
        return False

    def __eq__(self, other) -> bool: # For x == y
        if self._year == other.year and self._term == other.term:
            return True
        return False

    def __ne__(self, other) -> bool: # For x != y OR x <> y
        if self._year == other.year and self._term == other.term:
            return False
        return True

    def __gt__(self, other) -> bool: # For x > y
        if self._year > other.year: return True
        if self._year < other.year: return False
        if self._term > other.term: return True
        return False

    def __ge__(self, other) -> bool: # For x >= y
        if self._year > other.year: return True
        if self._year < other.year: return False
        if self._term >= other.term: return True
        return False

    # Saves the term in the database
    def save(self) -> None:
        g.db.execute('insert or ignore into Sessions(year, term) values (?, ?)', self._year,
                self._term)
