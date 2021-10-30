'''
You will write, at minimum, 6 unit tests for the script clean.py in part 1.
Each unit test should test one of the following constraints:
1. Posts that don’t have either 'title' or 'title_text' should be removed.
2. createdAt dates that don’t pass the ISO datetime standard should be removed.
3. Any lines that contain invalid JSON dictionaries should be ignored.
4. Any lines for which 'author' is null, N/A or empty should be removed.
5. total_count is a string containing a cast-able number, total_count is cast to an int properly.
6. The tags field gets split on spaces when given a tag containing THREE words (e.g., “nba basketball game”).

All tests should be (test) methods contained in one CleanTest class, sitting in a file called test_clean.py.
'''

import unittest
from pathlib import Path
import os, sys
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)
import json
from src.clean import clean_title, clean_date, clean_invalid, clean_author, clean_total_count, clean_tags

class CleanTest(unittest.TestCase):
    # You might want to load the fixture files as variables, and test your code against them. Check the fixtures folder.
    def setUp(self):
        # test directory path
        self.test_path = os.path.join(parentdir, 'test')
        
        # fixture file paths
        self.fixture1_path = os.path.join(self.test_path, 'fixtures', 'test_1.json')
        self.fixture2_path = os.path.join(self.test_path, 'fixtures', 'test_2.json')
        self.fixture3_path = os.path.join(self.test_path, 'fixtures', 'test_3.json')
        self.fixture4_path = os.path.join(self.test_path, 'fixtures', 'test_4.json')
        self.fixture5_path = os.path.join(self.test_path, 'fixtures', 'test_5.json')
        self.fixture6_path = os.path.join(self.test_path, 'fixtures', 'test_6.json')

        # load fixture files as dictionaries
        with open(self.fixture1_path, 'r') as f:
            f_line = f.readline()
            self.fixture1 = json.loads(f_line)
            
        with open(self.fixture2_path, 'r') as f:
            f_line = f.readline()
            self.fixture2 = json.loads(f_line)
            
        # file line string, not dictionary
        with open(self.fixture3_path, 'r') as f:
            f_line = f.readline()
            self.fixture3 = f_line
            
        with open(self.fixture4_path, 'r') as f:
            f_line = f.readline()
            self.fixture4 = json.loads(f_line)
            
        with open(self.fixture5_path, 'r') as f:
            f_line = f.readline()
            self.fixture5 = json.loads(f_line)
            
        with open(self.fixture6_path, 'r') as f:
            f_line = f.readline()
            self.fixture6 = json.loads(f_line)

    # 1: title
    def test_title(self):
        self.assertIsNone(clean_title(self.fixture1))
                
    # 2: date
    def test_date(self):
        self.assertIsNone(clean_date(self.fixture2))

    # 3: invalid
    def test_invalid(self):
        self.assertIsNone(clean_invalid(self.fixture3))

    # 4: author
    def test_author(self):
        self.assertIsNone(clean_author(self.fixture4))
        
    # 5: total_count
    def test_total_count(self):
        self.assertIsNone(clean_total_count(self.fixture5))

    # 6: tags
    # the tags field gets split on spaces when given a tag containing THREE words
    def test_tags(self):
        d = clean_tags(self.fixture6)
        self.assertEqual(len(d['tags']), 4)



if __name__ == '__main__':
    unittest.main()
