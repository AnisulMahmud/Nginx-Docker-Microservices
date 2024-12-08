import unittest
import requests
import time

class TestMetrics(unittest.TestCase):
    BASE_URL = "http://nginx:8197"  
    

    def test_get_metrics(self):
        """Test GET /metrics to check the metrics data."""

        #  check initial metrics
        response = requests.get(f"{self.BASE_URL}/metrics", auth=("anisul-mahmud", "docker"))
        self.assertEqual(response.status_code, 200)
        initial_metrics = response.json()

        # Extract initial uptime 
        initial_uptime = float(initial_metrics.get('Uptime (seconds)'))

        # Wait for a short time
        time.sleep(1)

        # Send another request
        response = requests.get(f"{self.BASE_URL}/metrics", auth=("anisul-mahmud", "docker"))
        self.assertEqual(response.status_code, 200)
        updated_metrics = response.json()

        # Extract updated uptime
        updated_uptime = float(updated_metrics.get('Uptime (seconds)'))

        # Test that uptime has increased 
        self.assertGreater(updated_uptime, initial_uptime, "Uptime did not increase correctly.")

if __name__ == "__main__":
    unittest.main()
