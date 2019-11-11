"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scraper.py
scrapes the handbook to get all of the information from it and put it in text form to then be parsed

"""
from bs4 import BeautifulSoup
import json
import requests
from typing import Callable, Dict, List, Optional

handbook_url = "https://www.handbook.unsw.edu.au"


class Scraper(object):
    def __init__(self, get_webpage: Callable[[str], str]):
        self.get_webpage = get_webpage

    def get_course_fields(self, year: int) -> List[str]:
        page = BeautifulSoup(self.get_webpage(handbook_url), 'html.parser')

        fields = []

        # The list of all fields (e.g. COMP) is in a div with the 'tab_educational_area' id
        fields_tab = page.find(id="tab_educational_area")

        assert fields_tab is not None

        # The fields are all in a tags
        field_tags = fields_tab.find_all('a')

        for field_tag in field_tags:
            # The name itself is in an h3 tag
            field_name_tag = field_tag.find('h3')
            field = field_name_tag.string
            # The field is formatted as "CODE: Name", so we get everything before the colon
            field_code = field.split(':')[0]

            # The field code should always be exactly 4 letters
            assert len(field_code) == 4

            fields.append(field_code)

        return fields

    # Given a field and a year, gets all of the course codes in that field
    # leave the field blank to get all codes in total
    def get_course_codes(self, year: int, field: str="", postgrad: bool=False) -> List[str]:
        if postgrad:
            study_level = "postgraduate"
        else:
            study_level = "undergraduate"

        url=handbook_url + f"/api/content/query/+contentType:subject%20-subject.published_in_handbook:0%20+subject.implementation_year:{year}%20+subject.code:*{field}*%20+subject.study_level:{study_level}%20+deleted:false%20+working:true/offset/0/limit/10000000/orderby/subject.code%20asc"


        try:
            response = self.get_webpage(url)
        except requests.exceptions.HTTPError:
            # Failed because there are no courses for that level at that field, return empty list
            return []

        results = json.loads(response)

        course_objects = results["contentlets"]

        codes = list(map(lambda x: x['code'], course_objects))

        return codes



def get_webpage(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.text

if __name__ == '__main__':
    scraper = Scraper(get_webpage)

    fields = scraper.get_course_fields(2019)

    for field in fields:
        print("Field is", field)

        codes = scraper.get_course_codes_for_field(2019, field, postgrad=False)
        print(field + ":", codes)
