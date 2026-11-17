import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import app as student_app


class IntegrationDashboardTests(unittest.TestCase):
    def setUp(self):
        self.database = tempfile.TemporaryDirectory()
        database_path = Path(self.database.name) / "students.db"

        def connect_to_test_database():
            connection = sqlite3.connect(database_path)
            connection.row_factory = sqlite3.Row
            return connection

        self.connection_factory = patch.object(
            student_app, "get_db_connection", connect_to_test_database
        )
        self.connection_factory.start()
        connection = connect_to_test_database()
        try:
            connection.execute(
                """CREATE TABLE students (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    name TEXT NOT NULL,
                    program TEXT NOT NULL,
                    year INTEGER NOT NULL,
                    section TEXT NOT NULL,
                    source TEXT DEFAULT 'Local'
                )"""
            )
        finally:
            connection.close()
        student_app.app.config["TESTING"] = True
        self.client = student_app.app.test_client()

    def tearDown(self):
        self.connection_factory.stop()
        self.database.cleanup()

    @patch.object(student_app.requests, "get")
    def test_partner_records_returns_remote_list(self, get):
        get.return_value = Mock(
            status_code=200,
            json=Mock(return_value=[{"student_id": "P-1"}]),
        )

        response = self.client.get("/partner-records")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [{"student_id": "P-1"}])

    @patch.object(student_app.requests, "get")
    def test_partner_records_rejects_non_list_response(self, get):
        get.return_value = Mock(status_code=200, json=Mock(return_value={"students": []}))

        response = self.client.get("/partner-records")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.get_json()["error"], "Partner API must return a JSON list")

    @patch.object(student_app.requests, "get")
    def test_partner_records_rejects_invalid_json(self, get):
        get.return_value = Mock(status_code=200, json=Mock(side_effect=ValueError))

        response = self.client.get("/partner-records")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.get_json()["error"], "Partner API did not return valid JSON")

    def test_saved_partner_record_keeps_partner_source(self):
        response = self.client.post(
            "/import-partner-student",
            data=json.dumps({
                "student_id": "P-1",
                "name": "Partner Student",
                "program": "BSIT",
                "year": 2,
                "section": "A",
                "source": "Untrusted value",
            }),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        records = self.client.get("/api/students").get_json()
        self.assertEqual(records[0]["source"], "Partner API")


if __name__ == "__main__":
    unittest.main()
