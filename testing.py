import unittest
import json
from setuptools import setup
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ikeascraper import Scrape

class TestIkeaScraper(TestCase):
    def setUp(self):
        self.obj_scraper = Scrape('chair')

    
    def test_get_links(self,
        mock_cookies: Mock,):
        self.obj_scraper.driver.get('https://www.ikea.com')
        self.obj_scraper.get_links()
        mock_cookies.assert_called_once()
        cookies_call_count = mock_cookies.call_count
        self.assertEqual(cookies_call_count, 1)

    # def test_length(self):
    #     length = len(self.handle.readlines())
    #     self.assertTrue(length > 50)

    # def valid_jsonfile(self, filename):
    #     try: 
    #         with open(filename) as f: 
    #             return json.load(f) 
    #     except ValueError as e: 
    #         print('invalid json: %s' % e) 
    #     return None

    def tearDown(self):
        self.obj_scraper.driver.quit()
        del self.obj_scraper   

TestIkeaScraper()
if __name__=='__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)