import importlib
import os
import tempfile
import unittest
from pathlib import Path

from fastapi.testclient import TestClient


class RagAssistantApiTests(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp_dir.cleanup)
        os.environ["UPLOAD_DIR"] = self.tmp_dir.name
        os.environ["EXPORT_DIR"] = os.path.join(self.tmp_dir.name, "exports")

        import app.main as main_module

        self.main_module = importlib.reload(main_module)
        self.client = TestClient(self.main_module.app)
        self.client.get("/health")

    def test_health_endpoint(self):
        response = self.client.get("/health")

        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertEqual(payload["status"], "healthy")
        self.assertIn("mode", payload)

    def test_upload_list_and_delete_flow(self):
        document_path = Path(self.tmp_dir.name) / "sample_document.txt"
        document_path.write_text(
            "This is a sample document for the RAG assistant regression test.",
            encoding="utf-8",
        )

        with document_path.open("rb") as handle:
            upload_response = self.client.post(
                "/upload",
                files={"file": ("sample_document.txt", handle, "text/plain")},
            )

        self.assertEqual(upload_response.status_code, 200)
        upload_payload = upload_response.json()
        self.assertEqual(upload_payload["document_id"], "sample_document.txt")
        self.assertGreaterEqual(upload_payload["chunks_processed"], 1)

        documents_response = self.client.get("/documents")
        self.assertEqual(documents_response.status_code, 200)
        documents_payload = documents_response.json()
        self.assertEqual(documents_payload["total"], 1)
        self.assertTrue(any(item["filename"] == "sample_document.txt" for item in documents_payload["documents"]))

        delete_response = self.client.delete("/documents/sample_document.txt")
        self.assertEqual(delete_response.status_code, 200)

        documents_after_delete = self.client.get("/documents")
        self.assertEqual(documents_after_delete.status_code, 200)
        self.assertEqual(documents_after_delete.json()["total"], 0)


if __name__ == "__main__":
    unittest.main()
