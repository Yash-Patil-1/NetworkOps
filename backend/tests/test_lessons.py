"""Tests for guided lessons API."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from fastapi.testclient import TestClient
from main import app


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestLessons:
    def test_list_lessons(self, client):
        r = client.get("/api/lessons")
        assert r.status_code == 200
        data = r.json()
        assert "lessons" in data
        assert len(data["lessons"]) >= 50  # at least 50 topics as lessons
        assert data["total"] > 100  # ~150 topics total

    def test_get_lesson_sections(self, client):
        r = client.get("/api/lessons/osi-model")
        assert r.status_code == 200
        data = r.json()
        assert len(data["sections"]) > 0
        assert "title" in data["sections"][0]
        assert "content" in data["sections"][0]

    def test_get_lesson_with_checkpoints(self, client):
        r = client.get("/api/lessons/ospf-fundamentals")
        assert r.status_code == 200
        data = r.json()
        # OSPF has 16 questions, so checkpoints should exist
        assert len(data["checkpoint_question_ids"]) >= 10

    def test_lesson_domain_info(self, client):
        r = client.get("/api/lessons/subnetting")
        assert r.status_code == 200
        data = r.json()
        assert "domain" in data
        assert "difficulty" in data

    def test_lesson_not_found(self, client):
        r = client.get("/api/lessons/nonexistent-topic")
        assert r.status_code == 404

    def test_complete_lesson_awards_xp(self, client):
        r = client.post("/api/lessons/osi-model/complete")
        assert r.status_code == 200
        data = r.json()
        assert data["status"] == "completed"
        assert data["xp_awarded"] == 15

    def test_complete_nonexistent_lesson(self, client):
        r = client.post("/api/lessons/nonexistent/complete")
        assert r.status_code == 404
