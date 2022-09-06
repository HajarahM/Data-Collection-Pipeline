import unittest
import json
from setuptools import setup
from unittest import TestCase
from unittest.mock import Mock, patch, call
from main import Scrape

class TestIkeaScraper(TestCase):
    def setUp(self):
        self.obj_scraper = Scrape('chair')

    @patch('ikeascraper.Scrape.get()')
    def test_launch_homepage(self, 
        mock_get: Mock,
        mock_find_element: Mock): # not sure what to test here yet
        self.obj_scraper.launch_homepage()
        # check if 'get' function is called twice
        mock_get.assert_called
        get_call_count = mock_get.call_count
        self.assetEqual(get_call_count, 2)
        

    def test_get_links(self):
        self.obj_scraper.get_links()
        

    def test_make_pdtfiles(self):
        self.obj_scraper.make_pdtfiles()
        

    @patch('ikeascraper.Scrape.stoprunning')
    def test_fetch(self):
        self.obj_scraper.fetch()
        
    

    

    
    # def test1_get_links(self,
    #     mock_cookies: Mock,):
    #     self.obj_scraper.driver.get('https://www.ikea.com')
    #     self.obj_scraper.get_links()

    # def test1_length(self):
    #     length = len(self.handle.readlines())
    #     self.assertTrue(length > 50)
    #
    # def sampletest(self):
    #     Arrange (goes into the setUp function)
    #     Act
    #     Assert

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


if __name__=='__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)