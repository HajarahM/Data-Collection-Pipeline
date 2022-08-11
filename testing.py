import unittest
import pathlib as pl
from setuptools import setup
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ikeascraper import Scrape


class TestIkeaScraper(TestCase):
    def setUp(self):
        self.obj_scraper = Scrape('chair')

    @patch('ikeascraper.Scrape.get')
    @patch('ikeascraper.Scrape.find_element')
    @patch('time.sleep')
    def test_launch_homepage(self, 
        mock_sleep: Mock,
        mock_find_element: Mock,
        mock_get: Mock
        ):

        self.obj_scraper.launch_homepage()
        # check if 'find_element' function is called with xpath
        mock_get.assert_called
        get_call_count = mock_get.call_count
        mock_find_element.assert_called_once_with(xpath='.//*[@class="website-link svelte-bdk5aj"]') # test if go-shopping button found
        mock_sleep.assert_has_calls[call(0.5), call(1)] # test sleep times called twice
        self.assertEqual(get_call_count, 2) # get_call called twice     
               

    def test_get_links(self):
        self.obj_scraper.launch_homepage()
        result_links = self.obj_scraper.get_links()        
        self.assertIsInstance(result_links, list) # list returned is in format 'list'
        self.assertEqual(len(result_links), 22) # number of items returned are 22
        

    def assertIsFile(self, path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))
    
    @patch('ikeascraper.Scrape._createFolder()')
    def test_make_pdtfiles(self,
        mock_createfolder: Mock):
        self.obj_scraper.make_pdtfiles()
        mock_createfolder('./raw_data/')
        path = pl.Path('./raw_data/') #test if raw_data file is created/exists
        self.assertIsFile(path)
        

    @patch('ikeascraper.Scrape.stoprunning')
    def test_fetch(self): # all methods here have been tested separately
        pass
     
    def tearDown(self):
        self.obj_scraper.driver.quit()
        del self.obj_scraper


if __name__=='__main__':
    unittest.main(argv=[''], verbosity=2, exit=True)