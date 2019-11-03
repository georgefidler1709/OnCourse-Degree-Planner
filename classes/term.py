"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

term.py
A term study period consisting of a year and a term 1-3 or summer term.

[MORE INFO ABOUT CLASS]
"""

from flask import g
from . import api

class Term(object):

    # define a new Term object
    # preconditions: (1 <= term <= 3)
    def __init__(self, year: int, term: int):
        self.year = year
        self.term = term

    def __repr__(self) -> str:
        return f"<Term year={self.year!r} term={self.term!r}>"

    def to_api(self) -> api.Term:
        return {"year": self.year,
                "term": self.term,
                }

    # Override comparison functions
    def __hash__(self) -> int:
        return hash((self.year, self.term))

    def __lt__(self, other) -> bool: # x < y
        if self.year < other.year: return True
        if self.year > other.year: return False
        if self.term < other.term: return True
        return False

    def __le__(self, other) -> bool: # For x <= y
        if self.year < other.year: return True
        if self.year > other.year: return False
        if self.term <= other.term: return True
        return False

    def __eq__(self, other) -> bool: # For x == y
        if self.year == other.year and self.term == other.term:
            return True
        return False

    def __ne__(self, other) -> bool: # For x != y OR x <> y
        if self.year == other.year and self.term == other.term:
            return False
        return True

    def __gt__(self, other) -> bool: # For x > y
        if self.year > other.year: return True
        if self.year < other.year: return False
        if self.term > other.term: return True
        return False

    def __ge__(self, other) -> bool: # For x >= y
        if self.year > other.year: return True
        if self.year < other.year: return False
        if self.term >= other.term: return True
        return False

    # Saves the term in the database
    def save(self) -> None:
        g.db.execute('insert or ignore into Sessions(year, term) values (?, ?)', self.year,
                self.term)
