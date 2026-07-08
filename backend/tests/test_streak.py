"""Tests for streak and XP logic."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from datetime import date, timedelta
import pytest
from fastapi.testclient import TestClient
from main import app
from models.database import get_connection


@pytest.fixture(autouse=True)
def clean_db():
    """Reset user_stats and daily_activity before each test."""
    conn = get_connection()
    conn.execute("DELETE FROM user_stats")
    conn.execute("DELETE FROM daily_activity")
    conn.execute("INSERT INTO user_stats (id, total_xp, current_streak, longest_streak, last_active_date) VALUES (1, 0, 0, 0, NULL)")
    conn.commit()
    conn.close()
    yield


def test_same_day_no_bump():
    """Activity on same day should not increase streak."""
    from services.stats import award_xp, XP_QUIZ_CORRECT

    r1 = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r1["current_streak"] == 1

    r2 = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r2["current_streak"] == 1  # same day, no bump


def test_consecutive_day_bump():
    """Activity on consecutive days should increase streak."""
    from services.stats import award_xp, XP_QUIZ_CORRECT

    # Day 1
    award_xp(XP_QUIZ_CORRECT, "quiz")

    # Manually set to yesterday to simulate next day
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (yesterday,))
    conn.commit()
    conn.close()

    r2 = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r2["current_streak"] == 2


def test_gap_resets_streak():
    """Missing a day should reset streak to 1."""
    from services.stats import award_xp, XP_QUIZ_CORRECT

    award_xp(XP_QUIZ_CORRECT, "quiz")

    # Simulate a 2-day gap
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (two_days_ago,))
    conn.commit()
    conn.close()

    r2 = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r2["current_streak"] == 1


def test_longest_never_decreases():
    """Longest streak should never decrease."""
    from services.stats import award_xp, XP_QUIZ_CORRECT

    award_xp(XP_QUIZ_CORRECT, "quiz")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (yesterday,))
    conn.commit()
    conn.close()
    r = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r["longest_streak"] >= 2

    # Reset and verify longest stays
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (two_days_ago,))
    conn.commit()
    conn.close()

    r = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r["longest_streak"] == 2
    assert r["current_streak"] == 1


def test_calculate_level():
    from services.stats import calculate_level

    assert calculate_level(0)["level"] == 1
    assert calculate_level(50)["level"] == 2
    assert calculate_level(120)["level"] == 3
    assert calculate_level(2000)["level"] == 10
    assert calculate_level(2000)["max_level_reached"] is True
    assert calculate_level(2500)["level"] == 10


def test_checkpoint_xp():
    """Quiz XP should be awarded correctly."""
    from services.stats import award_xp, XP_QUIZ_CORRECT

    r = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r["total_xp"] == XP_QUIZ_CORRECT

    r2 = award_xp(XP_QUIZ_CORRECT, "quiz")
    assert r2["total_xp"] == XP_QUIZ_CORRECT * 2


class TestStreakAPI:
    def test_get_streak(self, client):
        r = client.get("/api/streak")
        assert r.status_code == 200
        data = r.json()
        assert "total_xp" in data
        assert "current_streak" in data
        assert "daily_goal" in data
        assert "last_7_days" in data
        assert len(data["last_7_days"]) == 7

    def test_quiz_answer_awards_xp(self, client):
        """Submitting a correct quiz answer should return XP and streak info."""
        # First clean up any state
        conn = get_connection()
        conn.execute("DELETE FROM user_stats")
        conn.execute("INSERT INTO user_stats (id, total_xp, current_streak, longest_streak, last_active_date) VALUES (1, 0, 0, 0, NULL)")
        conn.commit()
        conn.close()

        # Get a question for osi-model
        q = client.get("/api/quiz/next?topic=osi-model")
        assert q.status_code == 200
        qid = q.json()["id"]

        # Submit answer containing "layer 3" (osi-model questions are about network layers)
        r = client.post("/api/quiz/answer", json={
            "question_id": qid,
            "topic_id": "osi-model",
            "answer": "layer 3"
        })
        assert r.status_code == 200
        data = r.json()
        assert "xp_awarded" in data
        assert "current_streak" in data
        assert "total_xp" in data

        # If correct, XP should be > 0; if wrong, streak should still be maintained
        if data["correct"]:
            assert data["xp_awarded"] == 5
        else:
            assert data["xp_awarded"] == 0
        assert data["current_streak"] >= 1


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
