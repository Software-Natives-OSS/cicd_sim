#!env python3
import unittest

from cicd_sim.git import Files

class TestGitFiles(unittest.TestCase):

    def test_get_unknown_file_content(self):
        files = Files()
        self.assertIsNone(files.get_file_content('unknownfile'))

    def test_set_content__read_back(self):
        files = Files()
        files.set_file_content('FileA', 'Content A')
        self.assertEqual('Content A', files.get_file_content('FileA'))

    def test_overwrite_content__read_back(self):
        files = Files()
        files.set_file_content('FileA', 'Content A')
        files.set_file_content('FileA', 'Content A 2')
        self.assertEqual('Content A 2', files.get_file_content('FileA'))

    def test_filename_with_special_chars(self):
        files = Files()
        file_name = 'The key is just the string. No special encoding is done !#@$>$#523'
        file_content = 'The File Content'
        files.set_file_content(file_name, file_content)
        self.assertEqual(file_content, files.get_file_content(file_name))
