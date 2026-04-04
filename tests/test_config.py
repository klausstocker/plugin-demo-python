import os
import sys
import unittest
import httpx

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from app.config import settings

class TestConfig(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def test_uris(self):
        self.assertEqual(settings.letto_plugin_uri_intern, "http://letto-plugindemo:8080/open")
        self.assertEqual(settings.letto_setup_uri, "http://letto-setup.nw-letto:8096")
    


if __name__ == '__main__':
    unittest.main()
