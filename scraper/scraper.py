"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scraper.py
scrapes the handbook to get all of the information from it and put it in text form to then be parsed

"""
from bs4 import BeautifulSoup
from typing import Callable, Dict

handbook_url = "https://www.handbook.unsw.edu.au"


class Scraper(object):
    def __init__(self, get_webpage: Callable[[str], str]):
        self.get_webpage = get_webpage

    def get_course_field_links(self, year: int) -> Dict[str, str]:
        page = BeautifulSoup(self.get_webpage(handbook_url), 'html.parser')

        field_links = {}

        # The list of all fields (e.g. COMP) is in a div with the 'tab_educational_area' id
        fields_tab = page.find(id="tab_educational_area")

        assert fields_tab is not None

        # The fields are all in a tags
        field_tags = fields_tab.find_all('a')

        for field_tag in field_tags:
            link = field_tag['href']

            # The name itself is in an h3 tag
            field_name_tag = field_tag.find('h3')
            field = field_name_tag.string
            # The field is formatted as "CODE: Name", so we get everything before the colon


            field_code = field.split(':')[0]

            # The field code should always be exactly 4 letters
            assert len(field_code) == 4

            field_links[field_code] = link

        return field_links


def get_webpage(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.text

if __name__ == '__main__':
    import requests

    scraper = Scraper(get_webpage)

    print(scraper.get_course_field_links(2019))
