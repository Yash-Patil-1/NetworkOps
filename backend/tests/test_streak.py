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
    from services.stats import record_activity

    r1 = record_activity("quiz")
    assert r1["current_streak"] == 1

    r2 = record_activity("quiz")
    assert r2["current_streak"] == 1  # same day, no bump


def test_consecutive_day_bump():
    """Activity on consecutive days should increase streak."""
    from services.stats import record_activity

    # Day 1
    record_activity("quiz")

    # Manually set to yesterday to simulate next day
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (yesterday,))
    conn.commit()
    conn.close()

    r2 = record_activity("quiz")
    assert r2["current_streak"] == 2


def test_gap_resets_streak():
    """Missing a day should reset streak to 1."""
    from services.stats import record_activity

    record_activity("quiz")

    # Simulate a 2-day gap
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (two_days_ago,))
    conn.commit()
    conn.close()

    r2 = record_activity("quiz")
    assert r2["current_streak"] == 1


def test_longest_never_decreases():
    """Longest streak should never decrease."""
    from services.stats import record_activity

    record_activity("quiz")
    yesterday = (date.today() - timedelta(days=1)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (yesterday,))
    conn.commit()
    conn.close()
    r = record_activity("quiz")
    assert r["longest_streak"] >= 2

    # Reset and verify longest stays
    two_days_ago = (date.today() - timedelta(days=2)).isoformat()
    conn = get_connection()
    conn.execute("UPDATE user_stats SET last_active_date = ?", (two_days_ago,))
    conn.commit()
    conn.close()

    r = record_activity("quiz")
    assert r["longest_streak"] == 2
    assert r["current_streak"] == 1


def test_calculate_level():
    """Level calculation: 10 levels, max at 2000 XP."""
    from services.stats import calculate_level

    assert calculate_level(0)["level"] == 1
    assert calculate_level(50)["level"] == 2
    assert calculate_level(120)["level"] == 3
    assert calculate_level(2000)["level"] == 10
    assert calculate_level(2000)["max_level_reached"] is True
    assert calculate_level(2500)["level"] == 10


def test_quiz_gives_no_xp():
    """Quiz activity should award 0 XP — only lessons earn XP."""
    from services.stats import record_activity, award_xp, XP_LESSON_COMPLETE

    # Quiz gives 0 XP
    r1 = record_activity("quiz")
    assert r1["total_xp"] == 0
    assert "xp_awarded" not in r1

    # Lesson gives XP
    r2 = award_xp(XP_LESSON_COMPLETE, "lesson")
    assert r2["total_xp"] == XP_LESSON_COMPLETE


def test_lesson_xp():
    """Lesson completion should award the correct XP."""
    from services.stats import award_xp, XP_LESSON_COMPLETE

    r = award_xp(XP_LESSON_COMPLETE, "lesson")
    assert r["total_xp"] == XP_LESSON_COMPLETE
    assert r["current_streak"] == 1

    r2 = award_xp(XP_LESSON_COMPLETE, "lesson")
    assert r2["total_xp"] == XP_LESSON_COMPLETE * 2


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

    def test_quiz_maintains_streak_no_xp(self, client):
        """Quiz answer should maintain streak but award 0 XP."""
        # Get a question for osi-model
        q = client.get("/api/quiz/next?topic=osi-model")
        assert q.status_code == 200
        qid = q.json()["id"]

        r = client.post("/api/quiz/answer", json={
            "question_id": qid,
            "topic_id": "osi-model",
            "answer": "layer 3"
        })
        assert r.status_code == 200
        data = r.json()
        assert data["xp_awarded"] == 0  # quizzes give 0 XP
        assert data["current_streak"] >= 1
        assert data["total_xp"] == 0  # no XP from quizzes


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c
