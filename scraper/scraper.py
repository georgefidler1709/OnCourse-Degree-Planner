"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

scraper.py
scrapes the handbook to get all of the information from it and put it in text form to then be parsed

"""
import bs4
from bs4 import BeautifulSoup
import json
import requests
from typing import Callable, Dict, List, Optional

from . import scrapedCourse

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
            study_level = "Postgraduate"
        else:
            study_level = "Undergraduate"

        lowercase_study_level = study_level.lower()

        url=handbook_url + f"/api/content/query/+contentType:subject%20-subject.published_in_handbook:0%20+subject.implementation_year:{year}%20+subject.code:*{field}*%20+subject.study_level:{lowercase_study_level}%20+deleted:false%20+working:true/offset/0/limit/10000000/orderby/subject.code%20asc"


        try:
            response = self.get_webpage(url)
        except requests.exceptions.HTTPError:
            # Failed because there are no courses for that level at that field, return empty list
            return []

        results = json.loads(response)

        course_objects = results["contentlets"]

        codes = list(map(lambda x: x['code'], course_objects))

        return codes

    # Scrape the given course for the given year and return it as a ScrapedCourse
    # (a course with all of the information unparsed in string form)
    def get_course(self, year: int, course_code: str,
            postgrad: bool=False) -> scrapedCourse.ScrapedCourse:
        if postgrad:
            study_level = 'Postgraduate'
        else:
            study_level = 'Undergraduate'

        lowercase_code = course_code.lower()
        lowercase_study_level = study_level.lower()

        url = handbook_url + f'/{lowercase_study_level}/courses/{year}/{lowercase_code}'

        page = BeautifulSoup(self.get_webpage(url), 'html.parser')

        # Get course name
        name_tag = page.find(attrs={'data-hbui':'module-title'})
        course_name = name_tag.string


        # Get units
        uoc_wrapper = page.find(attrs={'data-credit-points':True})
        uoc_tag = uoc_wrapper.find(class_='hide-lg').find('strong')
        uoc = uoc_tag.string

        units_number, uoc_text = uoc.split(' ')
        assert uoc_text == 'UOC'

        units = int(units_number)



        # Get overview
        overview_wrapper = page.find(id='subject-intro')
        overview_tag = overview_wrapper.find(class_='readmore__wrapper')
        overview = overview_tag.encode_contents()

        # Get equivalents and exclusions
        equivalent_section = page.find(id='equivalence-rules')
        equivalents = self.find_courses_from_section(equivalent_section)

        exclusion_section = page.find(id='exclusion-rules')
        exclusions = self.find_courses_from_section(exclusion_section)

        requirements_section = page.find(id='SubjectConditions')
        if requirements_section is None:
            requirements = ''
        else:
            requirements_wrapper = requirements_section.find(class_='a-card-text')
            requirements_tag = requirements_wrapper.find('div')
            requirements = requirements_tag.string


        faculty = ''
        school = ''
        terms = ''

        # Faculty, school, study level and terms are all in an attributes table
        attributes_table = page.find(class_='o-attributes-table')
        attributes = attributes_table.find_all(class_='o-attributes-table-item')
        for attribute in attributes:
            name_tag = attribute.contents[1]
            value_tag = attribute.contents[3]
            attr_name = name_tag.string
            value = value_tag.string
            if attr_name == 'Faculty':
                faculty = value
            elif attr_name == 'School':
                school = value
            elif attr_name == 'Study Level':
                # Just make sure that we have the right study level for sanity
                if value != study_level:
                    raise ValueError(f'''Expected study level {study_level} should be equal to actual study
                    level {value}''')
            elif attr_name == 'Offering Terms':
                terms = value


        return scrapedCourse.ScrapedCourse(year=year, code=course_code, name=course_name, units=units, overview=overview,
                equivalents=equivalents,
                exclusions=exclusions, requirements=requirements, faculty=faculty, school=school, study_level=study_level,
                terms=terms)

    def find_courses_from_section(self, section: bs4.element.Tag):
        if section is None:
            return []
        else:
            course_sections = section.find_all(class_='m-single-course-top-row')

            courses = list(map(lambda x: x.find('span'), course_sections))
            return list(map(lambda x: x.string, courses))


def get_webpage(url):
    response = requests.get(url)
    response.raise_for_status()

    return response.text

if __name__ == '__main__':
    scraper = Scraper(get_webpage)

    fields = scraper.get_course_fields(2019)

    course = scraper.get_course(2020, "COMP1511")

    '''

    for field in fields:
        print("Field is", field)

        codes = scraper.get_course_codes_for_field(2019, field, postgrad=False)
        print(field + ":", codes)

    '''
