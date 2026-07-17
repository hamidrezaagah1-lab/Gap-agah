
import os
import tempfile
import unittest
from unittest.mock import patch

from core import storage
from web_app import app


class TestWebApp(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        storage.DB_PATH = self.db_path
        storage.init_db()

        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        os.close(self.db_fd)
        if os.path.exists(self.db_path):
            os.remove(self.db_path)

    def test_index_get(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_index_post_saves_chat(self):
        with patch("web_app.framework.process") as mock_process:
            mock_process.return_value = {
                "status": "success",
                "response": "پاسخ آزمایشی",
                "mode": "general",
            }

            response = self.client.post(
                "/",
                data={"prompt": "سلام", "mode": "general"},
                follow_redirects=True,
            )

            self.assertEqual(response.status_code, 200)
            self.assertIn("پاسخ آزمایشی".encode("utf-8"), response.data)

            with self.client.session_transaction() as session_data:
                session_id = session_data["session_id"]

            history = storage.get_history(session_id)
            self.assertEqual(len(history), 1)
            self.assertEqual(history[0]["prompt"], "سلام")
            self.assertEqual(history[0]["response"], "پاسخ آزمایشی")
            self.assertEqual(history[0]["mode"], "general")

    def test_clear_history(self):
        with self.client.session_transaction() as session_data:
            session_data["session_id"] = "test-session"

        storage.save_chat("test-session", "سوال", "جواب", "general")

        response = self.client.post("/clear", follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        history = storage.get_history("test-session")
        self.assertEqual(history, [])


if __name__ == "__main__":
    unittest.main()
