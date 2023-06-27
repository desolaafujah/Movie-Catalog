import unittest
from unittest.mock import patch
from io import StringIO
import sys

from movies.py import getData


class TestYourCode(unittest.TestCase):
    def test_getData(self):
        result = getData("India")
        self.assertIsNotNone(result)
        self.assertEqual(result["response"][0]["country"], "India")
        self.assertEqual(result["response"][0]["continent"], "Asia")
        self.assertEqual(result["response"][0]["cases"]["total"], 44993999)
        self.assertEqual(result["response"][0]["cases"]["active"], 1655)
        self.assertEqual(result["response"][0]["cases"]["recovered"], 44460441)
        self.assertEqual(result["response"][0]["cases"]["critical"], 531903)
        self.assertEqual(result["response"][0]["deaths"]["total"], None)


if __name__ == '__main__':
    unittest.main()