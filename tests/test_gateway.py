import unittest
import requests


class TestAPIGateway(unittest.TestCase):
    # BASE_URL = "http://localhost:8198" 
    BASE_URL = "http://nginx:80"

    def test_get_state(self):
        """Test GET /state to retrieve current system states."""
        response = requests.get(f"{self.BASE_URL}/state", auth=("anisul-mahmud", "docker"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.text, ["INIT", "RUNNING", "PAUSED", "SHUTDOWN"], "Unexpected state")

    def test_put_state_running(self):
        """Test PUT /state to set system to RUNNING."""
        response = requests.put(f"{self.BASE_URL}/state", data="RUNNING", auth=("anisul-mahmud", "docker"))
        self.assertIn(response.status_code, [200, 403])
        if response.status_code == 403:
            self.assertIn("Login required", response.text, "Expected login required response")
        else:
            self.assertIn("State changed to RUNNING", response.text, "Unexpected response for state change")

    def test_put_state_init(self):
        """Test PUT /state to reset system to INIT."""
        response = requests.put(f"{self.BASE_URL}/state", data="INIT", auth=("anisul-mahmud", "docker"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("State changed to INIT", response.text, "Unexpected response for INIT state")

    def test_get_run_log(self):
        """Test GET /run-log to retrieve the system's state transitions."""
        response = requests.get(f"{self.BASE_URL}/run-log", auth=("anisul-mahmud", "docker"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.text) > 0, "Run log should not be empty")

    def test_get_request(self):
        """Test GET /request to ensure response when the system is RUNNING."""
        # Ensure the system is in RUNNING state
        requests.put(f"{self.BASE_URL}/state", data="RUNNING", auth=("anisul-mahmud", "docker"))

        response = requests.get(f"{self.BASE_URL}/request", auth=("anisul-mahmud", "docker"))
        if response.status_code == 403:
            self.assertIn("Service2 is not in RUNNING state", response.text, "Unexpected response for Service2 state")
        else:
            self.assertEqual(response.status_code, 200)
            self.assertIn("IP Address", response.json(), "Unexpected response format for /request")

    # def test_put_state_shutdown(self):
    #     """Test PUT /state to set system to SHUTDOWN."""
    #     response = requests.put(f"{self.BASE_URL}/state", data="SHUTDOWN", auth=("anisul-mahmud", "docker"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn("State changed to SHUTDOWN", response.json().get("message", ""), "Unexpected response for SHUTDOWN state")



if __name__ == "__main__":
    unittest.main()
