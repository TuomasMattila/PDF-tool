"""
This test suite needs to be run from the root directory of the project.
Example command for executing (while being in the directory where main.py is):
py -m pdf_tool.tests.tests
"""
import unittest
import pypdf
from pdf_tool import utils

class Tests(unittest.TestCase):

    def test_generate_bookmarks(self):
        pass

    def test_get_pdf_reader(self):
        pass

    def test_name_new_pdf(self):
        pass

if __name__ == '__main__':
    unittest.main()