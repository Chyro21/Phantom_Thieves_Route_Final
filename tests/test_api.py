import unittest
from app import app

class ApiSmokeTests(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["project"], "Phantom Thieves Route")

    def test_docs(self):
        response = self.client.get("/api/docs")
        self.assertEqual(response.status_code, 200)
        paths = [item["path"] for item in response.get_json()["endpoints"]]
        self.assertIn("/api/activities", paths)

    def test_create_requires_json(self):
        response = self.client.post("/api/activities", data="not json", content_type="text/plain")
        self.assertEqual(response.status_code, 400)

    def test_create_requires_activity_name(self):
        response = self.client.post("/api/activities", json={"category": "Study"})
        self.assertEqual(response.status_code, 400)

    def test_boss_requires_date(self):
        response = self.client.get("/api/bosses")
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()
