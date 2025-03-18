import unittest
import json
from app import app

class TestTextAnalysis(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_analyze_text(self):
        response = self.client.post("/analyze", json={"text": "buy now"})
        data = json.loads(response.data)
        self.assertTrue(0 <= data["bot_score"] <= 1)

if __name__ == "__main__":
    unittest.main()
