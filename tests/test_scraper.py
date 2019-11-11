"""
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_scraper.py
Test the functions defined in scraper.py

"""

import pytest

from scraper import scraper

handbook_url = "https://www.handbook.unsw.edu.au"

# This just contains a mapping of urls to pages, for testing the scraper
class MockRequests:
    def __init__(self):
        self.pages = {}

    def add_page(self, url: str, page: str):
        self.pages[url] = page

    def get_webpage(self, url: str):
        return self.pages.get(url, None)

class TestScraper():
    def setup_method(self, function):
        self.requests = MockRequests()
        self.scraper = scraper.Scraper(self.requests.get_webpage)

class TestScraper_GetCourseFieldLinks(TestScraper):
    # Testing when the request fails for some reason, should raise exception
    def test_failed_request(self):
        try:
            self.scraper.get_course_field_links(2019)
            assert "Should not have raised exception" == 1
        except:
            pass

    def test_single_course_link(self):
        page = '''
<div class="a-browse-tile-container p-left-0 p-right-0" id="tab_educational_area" data-controlled-by="educational_areaControl" data-active="true" role="tabpanel" aria-labelledby="educational_areaControl">
  <a class="a-browse-tile  a-browse-tile--header-only" href="/testlink">
      <div class="a-browse-tile-header">
          <h3 class="h4">TEST: Testing</h3>
          <i class="a-icon" aria-hidden="true">arrow_forward</i>
      </div>
  </a>
</div>
'''
        self.requests.add_page(handbook_url, page)

        links = self.scraper.get_course_field_links(2019)

        assert links['TEST'] == '/testlink'

    def test_multiple_course_link(self):
        page = '''
<div class="a-browse-tile-container p-left-0 p-right-0" id="tab_educational_area" data-controlled-by="educational_areaControl" data-active="true" role="tabpanel" aria-labelledby="educational_areaControl">
  <a class="a-browse-tile  a-browse-tile--header-only" href="/testlink1">
      <div class="a-browse-tile-header">
          <h3 class="h4">TEST: Testing</h3>
          <i class="a-icon" aria-hidden="true">arrow_forward</i>
      </div>
  </a>
  <a class="a-browse-tile  a-browse-tile--header-only" href="/testlink2">
      <div class="a-browse-tile-header">
          <h3 class="h4">COMP: Computing</h3>
          <i class="a-icon" aria-hidden="true">arrow_forward</i>
      </div>
  </a>
</div>
'''
        self.requests.add_page(handbook_url, page)

        links = self.scraper.get_course_field_links(2019)

        assert links['TEST'] == '/testlink1'
        assert links['COMP'] == '/testlink2'

