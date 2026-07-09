
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as c: yield c

class TestHealth:
    def test_root(self, client): assert client.get("/").json()["name"] == "NetworkOps"
    def test_health(self, client): assert client.get("/health").json()["status"] == "healthy"

class TestTopics:
    def test_list(self, client):
        r = client.get("/api/topics"); assert r.status_code == 200 and r.json()["total"] >= 4
    def test_search(self, client):
        r = client.get("/api/topics/search?q=dns"); assert r.json()["total"] >= 1
    def test_get(self, client):
        r = client.get("/api/topics/osi-model"); assert r.status_code == 200
    def test_404(self, client):
        assert client.get("/api/topics/nonexistent").status_code == 404

class TestQuiz:
    def test_next_question(self, client):
        r = client.get("/api/quiz/next?topic=osi-model"); assert r.status_code == 200 and "question" in r.json()
    def test_submit_answer(self, client):
        q = client.get("/api/quiz/next?topic=osi-model").json()
        r = client.post("/api/quiz/answer", json={"question_id": q["id"], "topic_id": "osi-model", "answer": "layer 3"})
        assert r.status_code == 200 and "correct" in r.json()
    def test_stats(self, client):
        r = client.get("/api/quiz/stats"); assert r.status_code == 200

class TestDomains:
    def test_list(self, client):
        r = client.get("/api/domains"); assert len(r.json()["domains"]) == 6
    def test_phases(self, client):
        r = client.get("/api/domains/phases"); assert len(r.json()["phases"]) == 6

class TestProgress:
    def test_get(self, client):
        r = client.get("/api/progress"); assert "total_topics" in r.json()
    def test_mark(self, client):
        r = client.post("/api/progress/mark", json={"topic_id": "osi-model"}); assert r.status_code == 200
