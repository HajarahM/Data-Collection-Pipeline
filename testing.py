import unittest
import json

class FileTestCase(unittest.TestCase):
    def setUp(self):
        self.handle = open("scraper.py", "r")

    def test_length(self):
        length = len(self.handle.readlines())
        self.assertTrue(length > 50)

    def valid_jsonfile(self, filename):
        try: 
            with open(filename) as f: 
                return json.load(f) 
        except ValueError as e: 
            print('invalid json: %s' % e) 
        return None


    def tearDown(self):
        self.handle.close()
    
unittest.main(argv=[''], verbosity=2, exit=False)