"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_term.py
Test the functions defined in term.py

[MORE INFO ABOUT CLASS]
"""

import pytest
from term import Term


"""
testing - will write formally later
"""
term12020 = Term(2020, 1)
term22020 = Term(2020, 2)
term32020 = Term(2020, 3)
term32019 = Term(2019, 3)
term22020v2 = Term (2020, 2)

# test lt
assert term12020 < term22020
assert term32019 < term12020
assert term32019 < term32020
assert not term22020 < term22020v2
assert not term32020 < term22020

# test le
assert term12020 <= term22020
assert term32019 <= term12020
assert term32019 <= term32020
assert term22020 <= term22020v2
assert not term32020 <= term22020

# test eq
assert term22020 == term22020
assert term22020 == term22020v2
assert term22020v2 == term22020
assert not term22020 == term12020
assert not term32020 == term32019

#test ne
assert term22020 != term12020
assert term32020 != term32019
assert not term22020 != term22020
assert not term22020 != term22020v2
assert not term22020v2 != term22020

# test gt
assert term22020 > term12020
assert term12020 > term32019
assert term32020 > term32019
assert not term22020v2 > term22020
assert not term22020 > term32020

# test ge
assert term22020 >= term12020
assert term12020 >= term32019
assert term32020 >= term32019
assert term22020v2 >= term22020
assert not term22020 >= term32020

