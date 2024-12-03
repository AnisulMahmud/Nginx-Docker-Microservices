import unittest
import requests
from requests.auth import HTTPBasicAuth

class TestAPIGateway(unittest.TestCase):
    def test_gateway_responds(self):
        # API Gateway URL
        url = "http://localhost:8198/api/"
        
        # Authentication credentials
        username = "anisul-mahmud"
        password = "docker"
        
        # Send request with authentication
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        
        # Debugging response
        print("Status Code:", response.status_code)
        print("Response Body:", response.text)
        
        # Assert response is successful
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
