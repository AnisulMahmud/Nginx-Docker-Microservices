import unittest
import requests

class TestServices(unittest.TestCase):
    def test_service1_request(self):
        response = requests.get("http://localhost:8199/api/request")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("Service1", data)
        self.assertIn("Service2", data)

    def test_service2_response(self):
        response = requests.get("http://localhost:8200/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ip_address", data)
        self.assertIn("processes", data)

if __name__ == "__main__":
    unittest.main()
