"""XP, level, and streak calculations for NetworkOps."""

from datetime import date, timedelta
from models.database import get_connection

# XP values
XP_LESSON_COMPLETE = 15
XP_QUIZ_CORRECT = 5
DAILY_GOAL = 50

# XP thresholds for levels 1–10
LEVEL_THRESHOLDS = [0, 50, 120, 220, 360, 550, 800, 1100, 1500, 2000]


def calculate_level(total_xp: int) -> dict:
    """Derive level info purely from XP."""
    level = 1
    for i, threshold in enumerate(LEVEL_THRESHOLDS):
        if total_xp >= threshold:
            level = i + 1

    if level >= len(LEVEL_THRESHOLDS):
        level_xp = 0
        next_level_xp = 1
        max_level_reached = True
    else:
        level_xp = total_xp - LEVEL_THRESHOLDS[level - 1]
        next_level_xp = LEVEL_THRESHOLDS[level] - LEVEL_THRESHOLDS[level - 1]
        max_level_reached = False

    return {
        "level": level,
        "level_xp": level_xp,
        "next_level_xp": next_level_xp,
        "max_level_reached": max_level_reached,
        "total_xp": total_xp,
        "level_thresholds": LEVEL_THRESHOLDS,
    }


def _update_streak_and_activity(amount: int, kind: str, conn) -> None:
    """Shared logic: update streak and daily_activity."""
    today = date.today()
    today_str = today.isoformat()
    yesterday_str = (today - timedelta(days=1)).isoformat()

    row = conn.execute("SELECT * FROM user_stats WHERE id = 1").fetchone()
    last_active = row["last_active_date"]

    if last_active == today_str:
        pass  # streak unchanged
    elif last_active == yesterday_str:
        conn.execute("UPDATE user_stats SET current_streak = current_streak + 1 WHERE id = 1")
    else:
        conn.execute("UPDATE user_stats SET current_streak = 1 WHERE id = 1")

    # Update longest streak
    cur = conn.execute("SELECT current_streak, longest_streak FROM user_stats WHERE id = 1").fetchone()
    if cur["current_streak"] > cur["longest_streak"]:
        conn.execute("UPDATE user_stats SET longest_streak = ? WHERE id = 1", (cur["current_streak"],))

    # Update XP and last active
    conn.execute(
        "UPDATE user_stats SET total_xp = total_xp + ?, last_active_date = ? WHERE id = 1",
        (amount, today_str)
    )

    # Upsert daily activity
    existing = conn.execute(
        "SELECT xp, lessons, quizzes FROM daily_activity WHERE date = ?", (today_str,)
    ).fetchone()
    if existing:
        lesson_inc = 1 if kind == "lesson" else 0
        quiz_inc = 1 if kind == "quiz" else 0
        conn.execute(
            "UPDATE daily_activity SET xp = xp + ?, lessons = lessons + ?, quizzes = quizzes + ? WHERE date = ?",
            (amount, lesson_inc, quiz_inc, today_str)
        )
    else:
        conn.execute(
            "INSERT INTO daily_activity (date, xp, lessons, quizzes) VALUES (?, ?, ?, ?)",
            (today_str, amount, 1 if kind == "lesson" else 0, 1 if kind == "quiz" else 0)
        )


def _build_response(conn) -> dict:
    """Build the standard stats response dict from current DB state."""
    today = date.today()
    today_str = today.isoformat()

    updated = conn.execute("SELECT * FROM user_stats WHERE id = 1").fetchone()
    today_activity = conn.execute(
        "SELECT xp FROM daily_activity WHERE date = ?", (today_str,)
    ).fetchone()

    level_info = calculate_level(updated["total_xp"])
    today_xp = today_activity["xp"] if today_activity else 0

    return {
        "total_xp": updated["total_xp"],
        "current_streak": updated["current_streak"],
        "longest_streak": updated["longest_streak"],
        "daily_goal": DAILY_GOAL,
        "today_xp": today_xp,
        "goal_met": today_xp >= DAILY_GOAL,
        **level_info,
    }


def award_xp(amount: int, kind: str) -> dict:
    """Award XP and update streak."""
    conn = get_connection()
    _update_streak_and_activity(amount, kind, conn)
    conn.commit()
    result = _build_response(conn)
    conn.close()
    return result


def get_streak() -> dict:
    """Get current streak and XP data for the dashboard."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM user_stats WHERE id = 1").fetchone()

    today = date.today()
    today_str = today.isoformat()

    today_activity = conn.execute(
        "SELECT xp FROM daily_activity WHERE date = ?", (today_str,)
    ).fetchone()
    today_xp = today_activity["xp"] if today_activity else 0

    # Last 7 days
    last_7 = []
    for i in range(6, -1, -1):
        d = (today - timedelta(days=i)).isoformat()
        act = conn.execute(
            "SELECT xp, lessons, quizzes FROM daily_activity WHERE date = ?", (d,)
        ).fetchone()
        last_7.append({
            "date": d,
            "xp": act["xp"] if act else 0,
            "lessons": act["lessons"] if act else 0,
            "quizzes": act["quizzes"] if act else 0,
        })

    conn.close()

    level_info = calculate_level(row["total_xp"])

    return {
        "total_xp": row["total_xp"],
        "current_streak": row["current_streak"],
        "longest_streak": row["longest_streak"],
        "daily_goal": DAILY_GOAL,
        "today_xp": today_xp,
        "goal_met": today_xp >= DAILY_GOAL,
        "last_7_days": last_7,
        **level_info,
    }


def record_activity(kind: str) -> dict:
    """Record activity (quiz, lesson) for streak tracking. Awards NO XP.
    Use this for quiz attempts where the answer is wrong — the streak is
    maintained but no XP is given."""
    conn = get_connection()
    _update_streak_and_activity(0, kind, conn)
    conn.commit()
    result = _build_response(conn)
    conn.close()
    return result
