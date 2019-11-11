from bs4 import BeautifulSoup
from typing import List, Callable

handbook_url = "https://www.handbook.unsw.edu.au"


class Scraper(object):
    def __init__(self, get_webpage: Callable[[str], str]):
        self.get_webpage = get_webpage

    def get_course_fields(self, year: int) -> List[str]:
        page = BeautifulSoup(self.get_webpage(handbook_url), 'html.parser')

        # The list of all fields (e.g. COMP) is in a div with the 'tab_educational_area' id
        fields_tab = page.find(id="tab_educational_area")

        assert fields_tab is not None

        # The fields are all in h3 tags
        field_tags = fields_tab.find_all('h3')

        fields = map(lambda x: x.string, field_tags)
        # The text in the fields is always FIELD:Field Name
        # So split on colon and take the first one
        fields = list(map(lambda x: x.split(':')[0], fields))

        print(fields)



if __name__ == '__main__':
    import requests

    get_webpage = lambda x: requests.get(x).text

    scraper = Scraper(get_webpage)

    scraper.get_course_fields(2019)
