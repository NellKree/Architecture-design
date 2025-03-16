import unittest

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

class TestNetworkAnalysis(unittest.TestCase):
    def test_analyze_network(self):
        response = client.post("/analyze_network", json={"connections": [["user1", "user2"], ["user2", "user3"]]})
        data = response.json()
        self.assertIn("clustering_coefficient", data)
        self.assertTrue(0 <= data["clustering_coefficient"] <= 1)

if __name__ == "__main__":
    unittest.main()
