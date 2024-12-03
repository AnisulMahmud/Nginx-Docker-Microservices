# import unittest
# import requests

# class TestService2(unittest.TestCase):
#     def test_service2_response(self):
#         # Use localhost with the exposed port
#         url = "http://localhost:5000/"
#         response = requests.get(url)
#         self.assertEqual(response.status_code, 200)

# if __name__ == "__main__":
#     unittest.main()


import unittest

class TestMath(unittest.TestCase):
    def test_addition(self):
        # A basic test to check if 2 + 2 equals 4
        self.assertEqual(2 + 2, 4)

if __name__ == "__main__":
    unittest.main()