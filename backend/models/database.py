import sqlite3
from pathlib import Path

DB_DIR = Path(__file__).parent.parent.parent / "data" / "database"
DB_PATH = DB_DIR / "networkops.db"

def get_connection() -> sqlite3.Connection:
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn

async def init_db():
    DB_DIR.mkdir(parents=True, exist_ok=True)
    conn = get_connection()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL UNIQUE,
            learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS quiz_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id TEXT NOT NULL,
            topic_id TEXT NOT NULL,
            correct INTEGER NOT NULL,
            user_answer TEXT,
            answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS quiz_seen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic_id TEXT NOT NULL,
            question_id TEXT NOT NULL,
            seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        CREATE TABLE IF NOT EXISTS user_stats (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            total_xp INTEGER NOT NULL DEFAULT 0,
            current_streak INTEGER NOT NULL DEFAULT 0,
            longest_streak INTEGER NOT NULL DEFAULT 0,
            last_active_date TEXT
        );
        INSERT OR IGNORE INTO user_stats (id) VALUES (1);
        CREATE TABLE IF NOT EXISTS daily_activity (
            date TEXT PRIMARY KEY,
            xp INTEGER NOT NULL DEFAULT 0,
            lessons INTEGER NOT NULL DEFAULT 0,
            quizzes INTEGER NOT NULL DEFAULT 0
        );
        CREATE INDEX IF NOT EXISTS idx_quiz_history_topic ON quiz_history(topic_id);
        CREATE INDEX IF NOT EXISTS idx_quiz_seen_topic ON quiz_seen(topic_id);
        CREATE INDEX IF NOT EXISTS idx_quiz_seen_question ON quiz_seen(question_id);
        CREATE INDEX IF NOT EXISTS idx_quiz_history_date ON quiz_history(answered_at);
    """)
    conn.commit()
    conn.close()
