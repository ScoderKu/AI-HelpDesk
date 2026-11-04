import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from app.knowledge import search_knowledge


class KnowledgeSearchTests(unittest.TestCase):
    def test_search_returns_bilingual_section_and_real_source_metadata(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "knowledge"
            root.mkdir()
            (root / "docker-guide.md").write_text(
                "# Docker troubleshooting\n\n"
                "- **Status:** verified project fact\n"
                "- **RAG Scope:** project-specific\n\n"
                "Docker Compose service DNS lets containers reach each other by service name.\n\n"
                "## Vianmääritys\n\n"
                "Kontin localhost tarkoittaa kyseistä konttia. Käytä palvelun nimeä verkossa.\n",
                encoding="utf-8",
            )
            with patch("app.knowledge.KNOWLEDGE_ROOT", root):
                results = search_knowledge("Docker Compose localhost kontti", limit=3)

        self.assertTrue(results)
        self.assertEqual(results[0]["source"], "knowledge/docker-guide.md")
        self.assertIn(results[0]["section"], {"Docker troubleshooting", "Vianmääritys"})
        self.assertGreater(results[0]["score"], 0)
        self.assertEqual(results[0]["status"], "verified project fact")

    def test_search_returns_empty_for_unmatched_query(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "guide.md").write_text(
                "# AI HelpDesk backend\n\n"
                "- **Status:** verified project fact\n"
                "- **RAG Scope:** project-specific\n\n"
                "The backend uses FastAPI and SQLAlchemy.\n",
                encoding="utf-8",
            )
            with patch("app.knowledge.KNOWLEDGE_ROOT", root):
                self.assertEqual(search_knowledge("quantum telescope", limit=3), [])

    def test_search_ignores_readme_and_non_markdown_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "README.md").write_text(
                "# Redis\n- **RAG Scope:** project-specific\nRedis cache\n",
                encoding="utf-8",
            )
            (root / "notes.csv").write_text("Redis cache", encoding="utf-8")
            with patch("app.knowledge.KNOWLEDGE_ROOT", root):
                self.assertEqual(search_knowledge("Redis cache"), [])

    def test_search_caps_result_limit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            for number in range(8):
                (root / f"doc-{number}.md").write_text(
                    f"# Project Redis cache {number}\n\n"
                    "- **Status:** verified project fact\n"
                    "- **RAG Scope:** project-specific\n\n"
                    "AI HelpDesk Redis cache TTL and key expiry.\n",
                    encoding="utf-8",
                )
            with patch("app.knowledge.KNOWLEDGE_ROOT", root):
                results = search_knowledge("Redis cache TTL", limit=99)
        self.assertLessEqual(len(results), 5)

    def test_search_excludes_general_reference_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "knowledge"
            root.mkdir()
            (root / "general.md").write_text(
                "# Python basics\n\n"
                "- **Status:** general technical guidance\n\n"
                "Python virtual environments isolate dependencies.\n",
                encoding="utf-8",
            )
            (root / "project.md").write_text(
                "# AI HelpDesk backend\n\n"
                "- **Status:** verified project fact\n"
                "- **RAG Scope:** project-specific\n\n"
                "The AI HelpDesk backend uses FastAPI and SQLAlchemy.\n",
                encoding="utf-8",
            )
            with patch("app.knowledge.KNOWLEDGE_ROOT", root):
                results = search_knowledge("Python FastAPI SQLAlchemy")
        self.assertTrue(results)
        self.assertEqual({item["source"] for item in results}, {"knowledge/project.md"})


if __name__ == "__main__":
    unittest.main()
