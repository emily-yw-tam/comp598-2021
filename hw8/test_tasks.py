'''
Write two unit tests for your code - one test for task 1, one for task 2.

For the first task, your unit test should pickup a mini script file and produce counts that are checked against a JSON file containing ground truth counts.

For the second task, your unit test should pickup the ground truth counts and compute TF-IDF scores that are checked against a JSON file containing ground truth TF-IDF scores.

In both cases, we will provide the mini script file, ground truth counts, and ground truth TF-IDF counts – so you will only write the inputs and the assertions to match your code. Crucially, your tests should import your python code and run it, *NOT* invoke a new python3 process.

Replace the assertions on test_task1 and test_task2 with any meaningful assertion. Just make sure you use the fixtures we provided; they will be under the variables self.mock_dialog, self.true_word_counts, self.true_tf_idfs. DELETE the self.assertTrue(True) you spot.

'''
import unittest
from pathlib import Path
import os, sys
import json
from os.path import dirname, abspath
parentdir = Path(__file__).parents[1]
sys.path.append(parentdir)

from src.compile_word_counts import get_dialog, get_words, get_word_counts
from src.compute_pony_lang import get_tfidfs # get_top_n_tfidfs

class TasksTest(unittest.TestCase):
    def setUp(self):
        dir = os.path.dirname(__file__)
        self.mock_dialog = os.path.join(dir, 'fixtures', 'mock_dialog.csv')
        self.true_word_counts = os.path.join(dir, 'fixtures', 'word_counts.true.json')
        self.true_tf_idfs = os.path.join(dir, 'fixtures', 'tf_idfs.true.json')
        
    def test_task1(self):
        # use  self.mock_dialog and self.true_word_counts; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        # code from main method of compile_word_counts.py
        ponies = ['twilight sparkle', 'applejack', 'rarity']
        punc = '()[],-.?!:;#&'
    
        df = get_dialog(self.mock_dialog, ponies, punc)

        parentdir = dirname(dirname(abspath(__file__)))
        stopwords_file = 'stopwords.txt'
        stopwords_path = os.path.join(parentdir, 'data', stopwords_file)
        
        word_list = get_words(df, stopwords_path, frequency=1)
        
        all_word_counts = {}
    
        for pony in ponies:
            all_word_counts[pony] = get_word_counts(df, word_list, pony)
            
        with open(self.true_word_counts, 'r') as f:
            all_word_counts_2 = json.load(f)
        
        print()
        print('TEST TASK 1')
        print('Check against a JSON file containing ground truth counts')
        self.assertEqual(all_word_counts, all_word_counts_2)
        print('OK')

    def test_task2(self):
        # use self.true_word_counts self.true_tf_idfs; REMOVE self.assertTrue(True) and write your own assertion, i.e. self.assertEquals(...)
        
        # code from main method of compute_pony_lang.py
        with open(self.true_word_counts, 'r') as f:
            all_word_counts = json.load(f)
        
        all_tfidfs = get_tfidfs(all_word_counts)
        
        with open(self.true_tf_idfs, 'r') as f2:
            all_tfidfs_2 = json.load(f2)
        
        print()
        print('TEST TASK 2')
        print('Check against a JSON file containing ground truth TF-IDF scores')
        self.assertEqual(all_tfidfs, all_tfidfs_2)
        print('OK')
        
    
    
if __name__ == '__main__':
    unittest.main()
