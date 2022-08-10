import unittest
import json
from setuptools import setup
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ikeascraper import Scrape

class TestIkeaScraper(TestCase):
    def setUp(self):
        self.obj_scraper = Scrape('chair')

    @patch('ikeascraper.Scrape.get()')
    def test_launch_homepage(self, 
        mock_get: Mock,
        mock_find_element: Mock): # not sure what to test here yet
        self.obj_scraper.launch_homepage()
        # check if 'find_element' function is called with xpath
        mock_get.assert_called
        get_call_count = mock_get.call_count
        self.assertEqual(get_call_count, 2)
        mock_find_element.assert_called
        

    def test_get_links(self):
        result = self.obj_scraper.get_links()        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 22)
        

    def test_make_pdtfiles(self):
        self.obj_scraper.make_pdtfiles()
        

    @patch('ikeascraper.Scrape.stoprunning')
    def test_fetch(self):
        self.obj_scraper.fetch()
     
    def tearDown(self):
        self.obj_scraper.driver.quit()
        del self.obj_scraper


if __name__=='__main__':
    unittest.main(argv=[''], verbosity=2, exit=False)