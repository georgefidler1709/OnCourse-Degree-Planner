'''
COMP4290 Group Project
Team: On Course
Alexander Rowell (z5116848), Eleni Dimitriadis (z5191013), Emily Chen (z5098910)
George Fidler (z5160384), Kevin Ni (z5025098)

test_scraper.py
Test the functions defined in scraper.py

'''

import os
import pytest
import requests
import sys
from typing import Dict

from scraper import scraper

handbook_url = 'https://www.handbook.unsw.edu.au'

# This just contains a mapping of urls to pages, for testing the scraper
class MockRequests:
    def __init__(self, base_url: str):
        self.pages: Dict[str, str] = {}
        self.base_url = base_url

    def add_page(self, url: str, page: str):
        self.pages[self.base_url + url] = page

    def get_webpage(self, url: str):
        if url in self.pages:
            return self.pages[url]
        else:
            print('Invalid url \n{}, urls are \n{}'.format(url, '\n'.join(self.pages.keys())))
            raise requests.exceptions.HTTPError('404')
        return self.pages.get(url, None)

class TestScraper():
    def setup_method(self, function):
        self.requests = MockRequests(handbook_url)
        self.scraper = scraper.Scraper(self.requests.get_webpage)

class TestScraper_GetCourseFields(TestScraper):
    # Testing when the request fails for some reason, should raise exception
    def test_failed_request(self):
        try:
            self.scraper.get_course_fields(2020)
            assert 'Should not have raised exception' == 1
        except:
            pass

    def test_single_field(self):
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

        fields = self.scraper.get_course_fields(2020)

        assert len(fields) == 1
        assert 'TEST' in fields

    def test_multiple_fields(self):
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

        fields = self.scraper.get_course_fields(2020)

        assert len(fields) == 2
        assert 'TEST' in fields
        assert 'COMP' in fields

class TestScraper_GetCourseCodes(TestScraper):
    # Testing when the request fails for some reason, should raise exception
    def test_failed_request(self):
        try:
            self.scraper.get_course_codes(2020, field='fake_field', postgrad=False)
            assert 'Should not have raised exception' == 1
        except:
            pass

    def test_single_undergraduate(self):
        page = '''{"contentlets":[{"credit_points":"6","study_level":"Undergraduate","modDate":"2019-10-02 03:05:27.178","code":"ACCT1501","keywords":"accounting","implementation_year":"2020","parent_academic_org":"5a3a1d4f4f4d97404aa6eb4f0310c77a","description":"<p>Unnecessarily long description.<\/p>","asced_broad":"dd350293db96df002e4c126b3a961909","inode":"775a4168-17b8-4a2c-ade1-df2729b946fd","sys_id":"e4b24457db26bf00358b403c3a961980","teaching_period":"bc067bf7db7993009c2c403c3a961994, 03067bf7db7993009c2c403c3a961997, 601633b7db7993009c2c403c3a9619ab","published_in_handbook":1,"academic_org":"d5a6242f4f0093004aa6eb4f0310c7d7","delivery_method":"Fully on-site","effective_date":"2020-01-01","host":"SYSTEM_HOST","stInode":"430aec14-28a7-403f-93b2-6bd63c9d9c8d","owner":"dotcms.org.1","identifier":"4755c028-67d6-4e1e-8556-99f5220ed8c1","owning_org":"d5a6242f4f0093004aa6eb4f0310c7d7","languageId":1,"active":"1","URL_MAP_FOR_CONTENT":"\/Undergraduate\/courses\/2020\/ACCT1501\/","study_level_value":"ugrd","version":"3","contact_hours":"3.5","teaching_period_display":"Term 1, Term 2, Term 3","folder":"SYSTEM_FOLDER","sortOrder":0,"modUser":"dotcms.org.1","name":"Accounting and Financial Management 1A","location":"6a49b4034f4d97404aa6eb4f0310c79b","status":"Active","content_type_label":"Course"}]}'''

        path = '/api/content/query/+contentType:subject%20-subject.published_in_handbook:0%20+subject.implementation_year:2020%20+subject.code:*ACCT*%20+subject.study_level:undergraduate%20+deleted:false%20+working:true/offset/0/limit/10000000/orderby/subject.code%20asc'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes(2020, field='ACCT', postgrad=False)
        assert len(results) == 1
        assert 'ACCT1501' in results

    def test_multiple_undergraduate(self):
        page = '''{"contentlets":[{"credit_points":"6","study_level":"Undergraduate","modDate":"2019-10-02 03:05:27.178","code":"ACCT1501","keywords":"accounting","implementation_year":"2020","parent_academic_org":"5a3a1d4f4f4d97404aa6eb4f0310c77a","description":"<p>The control.<\/p>","asced_broad":"dd350293db96df002e4c126b3a961909","inode":"775a4168-17b8-4a2c-ade1-df2729b946fd","sys_id":"e4b24457db26bf00358b403c3a961980","teaching_period":"bc067bf7db7993009c2c403c3a961994, 03067bf7db7993009c2c403c3a961997, 601633b7db7993009c2c403c3a9619ab","published_in_handbook":1,"academic_org":"d5a6242f4f0093004aa6eb4f0310c7d7","delivery_method":"Fully on-site","effective_date":"2020-01-01","host":"SYSTEM_HOST","stInode":"430aec14-28a7-403f-93b2-6bd63c9d9c8d","owner":"dotcms.org.1","identifier":"4755c028-67d6-4e1e-8556-99f5220ed8c1","owning_org":"d5a6242f4f0093004aa6eb4f0310c7d7","languageId":1,"active":"1","URL_MAP_FOR_CONTENT":"\/Undergraduate\/courses\/2020\/ACCT1501\/","study_level_value":"ugrd","version":"3","contact_hours":"3.5","teaching_period_display":"Term 1, Term 2, Term 3","folder":"SYSTEM_FOLDER","sortOrder":0,"modUser":"dotcms.org.1","name":"Accounting and Financial Management 1A","location":"6a49b4034f4d97404aa6eb4f0310c79b","status":"Active","content_type_label":"Course"},{"credit_points":"6","study_level":"Undergraduate","modDate":"2019-10-02 03:05:37.205","code":"ACCT1511","keywords":"accounting","implementation_year":"2020","parent_academic_org":"5a3a1d4f4f4d97404aa6eb4f0310c77a","description":"description_long","asced_broad":"dd350293db96df002e4c126b3a961909","inode":"b8c313fe-d587-4e32-8577-a5d7bbaaea70","sys_id":"5277f586db03b700038cc4048a961925","teaching_period":"b8f53777db7993009c2c403c3a9619e4, bc067bf7db7993009c2c403c3a961994, 03067bf7db7993009c2c403c3a961997, 601633b7db7993009c2c403c3a9619ab","published_in_handbook":1,"academic_org":"d5a6242f4f0093004aa6eb4f0310c7d7","delivery_method":"Fully on-site","effective_date":"2020-01-01","host":"SYSTEM_HOST","stInode":"430aec14-28a7-403f-93b2-6bd63c9d9c8d","owner":"dotcms.org.1","identifier":"787552f6-2358-4134-a9cb-c1c7a2862603","owning_org":"d5a6242f4f0093004aa6eb4f0310c7d7","languageId":1,"active":"1","URL_MAP_FOR_CONTENT":"\/Undergraduate\/courses\/2020\/ACCT1511\/","study_level_value":"ugrd","version":"5","contact_hours":"3","teaching_period_display":"Summer Term, Term 1, Term 2, Term 3","folder":"SYSTEM_FOLDER","sortOrder":0,"modUser":"dotcms.org.1","name":"Accounting and Financial Management 1B","location":"6a49b4034f4d97404aa6eb4f0310c79b","status":"Active","content_type_label":"Course"}]}'''

        path = '/api/content/query/+contentType:subject%20-subject.published_in_handbook:0%20+subject.implementation_year:2020%20+subject.code:*ACCT*%20+subject.study_level:undergraduate%20+deleted:false%20+working:true/offset/0/limit/10000000/orderby/subject.code%20asc'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes(2020, field='ACCT', postgrad=False)
        assert len(results) == 2
        assert 'ACCT1501' in results
        assert 'ACCT1511' in results

    def test_single_postgraduate(self):
        page = '''{"contentlets":[{"credit_points":"6","study_level":"Postgraduate","modDate":"2019-10-02 03:05:27.178","code":"ACCT1501","keywords":"accounting","implementation_year":"2020","parent_academic_org":"5a3a1d4f4f4d97404aa6eb4f0310c77a","description":"<p>Unnecessarily long description.<\/p>","asced_broad":"dd350293db96df002e4c126b3a961909","inode":"775a4168-17b8-4a2c-ade1-df2729b946fd","sys_id":"e4b24457db26bf00358b403c3a961980","teaching_period":"bc067bf7db7993009c2c403c3a961994, 03067bf7db7993009c2c403c3a961997, 601633b7db7993009c2c403c3a9619ab","published_in_handbook":1,"academic_org":"d5a6242f4f0093004aa6eb4f0310c7d7","delivery_method":"Fully on-site","effective_date":"2020-01-01","host":"SYSTEM_HOST","stInode":"430aec14-28a7-403f-93b2-6bd63c9d9c8d","owner":"dotcms.org.1","identifier":"4755c028-67d6-4e1e-8556-99f5220ed8c1","owning_org":"d5a6242f4f0093004aa6eb4f0310c7d7","languageId":1,"active":"1","URL_MAP_FOR_CONTENT":"\/Postgraduate\/courses\/2020\/ACCT1501\/","study_level_value":"ugrd","version":"3","contact_hours":"3.5","teaching_period_display":"Term 1, Term 2, Term 3","folder":"SYSTEM_FOLDER","sortOrder":0,"modUser":"dotcms.org.1","name":"Accounting and Financial Management 1A","location":"6a49b4034f4d97404aa6eb4f0310c79b","status":"Active","content_type_label":"Course"}]}'''

        path = '/api/content/query/+contentType:subject%20-subject.published_in_handbook:0%20+subject.implementation_year:2020%20+subject.code:*ACCT*%20+subject.study_level:postgraduate%20+deleted:false%20+working:true/offset/0/limit/10000000/orderby/subject.code%20asc'
        self.requests.add_page(path, page)

        results = self.scraper.get_course_codes(2020, field='ACCT', postgrad=True)
        assert len(results) == 1
        assert 'ACCT1501' in results

class TestScraper_GetCourse(TestScraper):
    def test_get_comp1511(self):
        from . import comp1511
        page = comp1511.text

        path = '/undergraduate/courses/2020/comp1511'

        self.requests.add_page(path, page)

        scraped_course = self.scraper.get_course(2020, 'COMP1511')

        assert scraped_course.year == 2020
        assert scraped_course.name == 'Programming Fundamentals'
        assert sorted(scraped_course.equivalents) == ['COMP1917', 'DPST1091']
        assert scraped_course.exclusions == ['DPST1091']
        assert scraped_course.requirements == ''
        assert scraped_course.faculty == 'Faculty of Engineering'
        assert scraped_course.school == 'School of Computer Science and Engineering'
        assert scraped_course.study_level == 'Undergraduate'
        assert len(scraped_course.terms) == 3
        assert scraped_course.units == 6

    def test_get_math1231(self):
        from . import math1231
        page = math1231.text

        path = '/undergraduate/courses/2020/math1231'

        self.requests.add_page(path, page)

        scraped_course = self.scraper.get_course(2020, 'MATH1231')

        assert scraped_course.year == 2020
        assert scraped_course.name == 'Mathematics 1B'
        assert sorted(scraped_course.equivalents) == ['DPST1014']
        assert sorted(scraped_course.exclusions) == ['DPST1014', 'MATH1021', 'MATH1241', 'MATH1251']
        assert scraped_course.requirements == 'Prerequisite: MATH1131 or DPST1013 or MATH1141'
        assert scraped_course.faculty == 'Faculty of Science'
        assert scraped_course.school == 'School of Mathematics & Statistics'
        assert scraped_course.study_level == 'Undergraduate'
        assert len(scraped_course.terms) == 3
        assert scraped_course.units == 6

