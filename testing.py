import unittest
import os
from setuptools import setup
from unittest import TestCase
from unittest.mock import Mock, patch, call
from ikeascraper import Scrape


class TestIkeaScraper(TestCase):   
    def setUp(self):
        self.obj_scraper = Scrape('chair')

    @patch('selenium.webdriver.remote.webdriver.WebDriver.get')
    @patch('selenium.webdriver.remote.webdriver.WebDriver.find_element')
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
        mock_find_element.assert_called_once_with(by='xpath', value='.//*[@class="website-link svelte-bdk5aj"]') # test if go-shopping button found
        mock_sleep.assert_has_calls(calls=[call(0.5), call(1)], any_order=True) # test sleep times called twice
        self.assertEqual(get_call_count, 2) # get_call called twice     
               
    def test_get_links(self):
        self.obj_scraper.launch_homepage()
        result_links = self.obj_scraper.get_links()        
        self.assertIsInstance(result_links, list) # list returned is in format 'list'
        self.assertEqual(len(result_links), 22) # number of items returned are 22
        

    def assertIsFile(self, path):
        if not os.path.exists(path) :
            raise AssertionError("File does not exist: %s" % str(path))  
        else: print(f"{str(path)} exists") 

    def test_make_pdtfiles(self):
        product_links = [
            'https://www.ikea.com/gb/en/p/kleppstad-wardrobe-with-2-doors-white-80437234/',
            'https://www.ikea.com/gb/en/p/vihals-storage-unit-white-90483268/',
            'https://www.ikea.com/gb/en/p/songesand-wardrobe-white-90347351/'
             ]
        dictionary_list = self.obj_scraper.make_pdtfiles('./raw_data/', product_links)
        self.assertIsInstance(dictionary_list, list) # list returned is in format 'list'
        self.assertEqual(len(dictionary_list), 3) # number of items returned are 3                    
        path = './raw_data/' #test if raw_data file is created/exists
        self.assertIsFile(path)
        path1 = './raw_data/ikeadata.json' #test if json file for list of dictionaries is created/exists
        self.assertIsFile(path1)
        

    # @patch('ikeascraper.Scrape.stoprunning')
    # def test_fetch(self): # all methods here have been tested separately
    #     pass
     
    def tearDown(self):
        self.obj_scraper.driver.quit()
        del self.obj_scraper


if __name__=='__main__':
    unittest.main(argv=[''], verbosity=2, exit=True)