import unittest
import requests

class TestService2(unittest.TestCase):
    def test_service2_response(self):
        url = "http://localhost:5000/"
        response = requests.get(url)
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
