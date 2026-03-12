import unittest
import os
from website_functions import *

class TestWebsiteFunctions(unittest.TestCase):
    def test_extract_title(self):
        markdown = "# My Title\n\nThis is some content."
        title = extract_title(markdown)
        self.assertEqual(title, "My Title")