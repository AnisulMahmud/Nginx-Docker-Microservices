import unittest
import requests

class TestService2(unittest.TestCase):
    def test_service2_response(self):
        url = "http://localhost:5000"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200, "Service2 should return HTTP 200 OK")
        self.assertIn("IP Address", response.json(), "Response should contain IP Address key")

if __name__ == "__main__":
    unittest.main()
