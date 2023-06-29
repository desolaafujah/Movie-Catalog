import unittest
from unittest.mock import patch
from io import StringIO
import sys
import sqlite3

from covid19 import getData, store


class TestYourCode(unittest.TestCase):
    def test_getData(self):
        result = getData("India")
        self.assertIsNotNone(result)
        self.assertEqual(result["response"][0]["country"], "India")
        self.assertEqual(result["response"][0]["continent"], "Asia")
        self.assertEqual(result["response"][0]["cases"]["total"], 44994032)
        self.assertEqual(result["response"][0]["cases"]["active"], 1606)
        self.assertEqual(result["response"][0]["cases"]["recovered"], 44460523)
        self.assertEqual(result["response"][0]["cases"]["critical"], None)
        self.assertEqual(result["response"][0]["deaths"]["total"], 531903)
    
    def setUp(self):
        self.conn = sqlite3.connect(":memory:")
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE country_data (id INTEGER PRIMARY KEY AUTOINCREMENT, country TEXT, cases INTEGER, count INTEGER)")
    
    def tearDown(self):
        self.conn.close()
    
    def test_store_existing_country(self):
        self.cursor.execute("INSERT INTO country_data (country, cases, count) VALUES (?, ?, ?)", ("Yemen", 200, 2))
        self.conn.commit()
        store("Yemen", {"response": [{"cases": {"total": 200}}]})
        self.cursor.execute("SELECT cases, count FROM country_data WHERE country=?", ("Yemen",))
        result = self.cursor.fetchone()
        self.assertEqual(result, (200, 2))


if __name__ == '__main__':
    unittest.main()