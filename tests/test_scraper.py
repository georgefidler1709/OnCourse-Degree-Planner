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
    def __init__(self, base_url: str):
        self.pages = {}
        self.base_url = base_url

    def add_page(self, url: str, page: str):
        self.pages[self.base_url + url] = page

    def get_webpage(self, url: str):
        return self.pages.get(url, None)

class TestScraper():
    def setup_method(self, function):
        self.requests = MockRequests(handbook_url)
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
        self.requests.add_page('', page)

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
        self.requests.add_page('', page)

        links = self.scraper.get_course_field_links(2019)

        assert links['TEST'] == '/testlink1'
        assert links['COMP'] == '/testlink2'

class TestScraper_GetCourseCodesForField(TestScraper):
    # Testing when the request fails for some reason, should raise exception
    def test_failed_request(self):
        try:
            self.scraper.get_course_codes_for_field('fake_path', 2019, postgrad=False)
            assert "Should not have raised exception" == 1
        except:
            pass

    def test_single_undergraduate(self):
        page = '''
<div class="m-tab-content" data-hbui="tab-content">
    <div class="a-browse-tile-container p-right-0 p-left-0"  id="Undergraduate" data-controlled-by="UndergraduateControl" data-active="true" style="border-bottom: 0" role="tabpanel" aria-label="Undergraduate panel">
      <h3 tabindex="0" id="subjectUndergraduateHeading" style="flex:1 0 100%" class="a-browse-tile-heading">Course </h3>
      <div class="a-browse-tile-container p-right-0 p-left-0"  style="flex:1 0 100%" id="subjectUndergraduate">
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/undergraduate/courses/2020/COMP1000/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 1 0 0 0, Introduction to World Wide Web, Spreadsheets and Databases . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP1000</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to World Wide Web, Spreadsheets and Databases</div>
          </div>
        </a>
      </div>
    </div>
</div>
'''
        path = 'COURSE_PATH'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes_for_field(path, 2019, postgrad=False)
        assert len(results) == 1
        assert 'COMP1000' in results

    def test_multiple_undergraduate(self):
        page = '''
<div class="m-tab-content" data-hbui="tab-content">
    <div class="a-browse-tile-container p-right-0 p-left-0"  id="Undergraduate" data-controlled-by="UndergraduateControl" data-active="true" style="border-bottom: 0" role="tabpanel" aria-label="Undergraduate panel">
      <h3 tabindex="0" id="subjectUndergraduateHeading" style="flex:1 0 100%" class="a-browse-tile-heading">Course </h3>
      <div class="a-browse-tile-container p-right-0 p-left-0"  style="flex:1 0 100%" id="subjectUndergraduate">
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/undergraduate/courses/2020/COMP1000/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 1 0 0 0, Introduction to World Wide Web, Spreadsheets and Databases . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP1000</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to World Wide Web, Spreadsheets and Databases</div>
          </div>
        </a>
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/undergraduate/courses/2020/COMP1511/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 1 5 1 1, Introduction to Computing . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP1511</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to Computing</div>
          </div>
        </a>
      </div>
    </div>
</div>
'''
        path = 'COURSE_PATH'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes_for_field(path, 2019, postgrad=False)
        assert len(results) == 2
        assert 'COMP1000' in results
        assert 'COMP1511' in results

    def test_single_postgraduate(self):
        page = '''
<div class="m-tab-content" data-hbui="tab-content">
    <div class="a-browse-tile-container p-right-0 p-left-0"  id="Postgraduate" data-controlled-by="PostgraduateControl" data-active="true" style="border-bottom: 0" role="tabpanel" aria-label="Postgraduate panel">
      <h3 tabindex="0" id="subjectPostgraduateHeading" style="flex:1 0 100%" class="a-browse-tile-heading">Course </h3>
      <div class="a-browse-tile-container p-right-0 p-left-0"  style="flex:1 0 100%" id="subjectPostgraduate">
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/postgraduate/courses/2020/COMP1000/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 1 0 0 0, Introduction to World Wide Web, Spreadsheets and Databases . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP1000</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to World Wide Web, Spreadsheets and Databases</div>
          </div>
        </a>
      </div>
    </div>
</div>
'''
        path = 'COURSE_PATH'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes_for_field(path, 2019, postgrad=True)
        assert len(results) == 1
        assert 'COMP1000' in results

    def test_undergraduate_and_postgraduate(self):
        page = '''
<div class="m-tab-content" data-hbui="tab-content">
    <div class="a-browse-tile-container p-right-0 p-left-0"  id="Undergraduate" data-controlled-by="UndergraduateControl" data-active="true" style="border-bottom: 0" role="tabpanel" aria-label="Undergraduate panel">
      <h3 tabindex="0" id="subjectUndergraduateHeading" style="flex:1 0 100%" class="a-browse-tile-heading">Course </h3>
      <div class="a-browse-tile-container p-right-0 p-left-0"  style="flex:1 0 100%" id="subjectUndergraduate">
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/undergraduate/courses/2020/COMP1000/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 1 0 0 0, Introduction to World Wide Web, Spreadsheets and Databases . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP1000</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to World Wide Web, Spreadsheets and Databases</div>
          </div>
        </a>
      </div>
    </div>
</div>

<div class="m-tab-content" data-hbui="tab-content">
    <div class="a-browse-tile-container p-right-0 p-left-0"  id="Postgraduate" data-controlled-by="PostgraduateControl" data-active="true" style="border-bottom: 0" role="tabpanel" aria-label="Postgraduate panel">
      <h3 tabindex="0" id="subjectPostgraduateHeading" style="flex:1 0 100%" class="a-browse-tile-heading">Course </h3>
      <div class="a-browse-tile-container p-right-0 p-left-0"  style="flex:1 0 100%" id="subjectPostgraduate">
        <a class="a-browse-tile a-browse-tile--list regular-border-top" href="/postgraduate/courses/2020/COMP1000/?browseBySubjectArea=91ce03204f0f5b00eeb3eb4f0310c782&" aria-label="2020 Course  C O M P 4 9 0 0, Introduction to World Wide Web, Spreadsheets and Databases . Worth 6 credit points">
          <div class="a-browse-tile-content with-separator">
            <div class="section">COMP4900</div>
            <div class="section uoc">6 UOC</div>
            <div class="section title">Introduction to World Wide Web, Spreadsheets and Databases</div>
          </div>
        </a>
      </div>
    </div>
</div>
'''
        path = 'COURSE_PATH'
        self.requests.add_page(path, page)

        undergrad_results = self.scraper.get_course_codes_for_field(path, 2019, postgrad=False)
        assert len(undergrad_results) == 1
        assert 'COMP1000' in undergrad_results

        postgrad_results = self.scraper.get_course_codes_for_field(path, 2019, postgrad=True)
        assert len(postgrad_results) == 1
        assert 'COMP4900' in postgrad_results
