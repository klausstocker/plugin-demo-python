import os
import sys
import unittest
import httpx

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

class TestEndpoints(unittest.TestCase):

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)

    def test_ping(self):
        response = httpx.get(
            url="http://localhost:8080/open/ping",
            timeout=10.0,
        )
        self.assertEqual(response.text, "pong")
    
    @unittest.skip('Work in progress')
    def test_gerneralinfo(self):
        response = httpx.post(
            url="http://localhost:8080/open/generalinfo",
            json={
                "pluginType": "Uhr1"
            },
            timeout=10.0,
        )
        self.assertEqual(response.text, "pong")

if __name__ == '__main__':
    unittest.main()
