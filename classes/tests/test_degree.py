import pytest

from classes.degree import Degree

@pytest.fixture
def compa1_shallow():
	deg = Degree(num_code=3778, name='Computer Science', year=2019,
		duration=3, faculty="Engineering", requirements=[], alpha_code='COMPA1')
	return deg


def test_url(compa1_shallow):
	url = compa1_shallow.get_url()

	assert url == "https://www.handbook.unsw.edu.au/undergraduate/programs/2019/3778"
