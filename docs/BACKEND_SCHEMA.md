# Backend Schema
## NetworkOps

---

## Topic JSON Schema
```json
{
  "id": "ospf-fundamentals",
  "domain": "network_engineering",
  "phase": 2,
  "name": "OSPF Fundamentals",
  "difficulty": "intermediate",
  "theory": {
    "what": "...",
    "why": "...",
    "how": "...",
    "when": "...",
    "key_concepts": ["..."],
    "configuration": "...",
    "troubleshooting": ["..."]
  },
  "related_topics": ["..."],
  "tags": ["routing", "igp"]
}
```

## Question JSON Schema
```json
{
  "id": "q-ospf-01",
  "topic_id": "ospf-fundamentals",
  "domain": "network_engineering",
  "type": "command|theory|scenario|troubleshooting",
  "difficulty": "easy|medium|hard",
  "question": "...",
  "correct_answers": ["..."],
  "validation_type": "exact|contains_all|contains_any",
  "required_keywords": ["..."],
  "explanation": "...",
  "hints": ["..."]
}
```

## SQLite Tables

### Progress
```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL UNIQUE,
    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Quiz History
```sql
CREATE TABLE quiz_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    correct INTEGER NOT NULL,
    user_answer TEXT,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Quiz Seen Queue
```sql
CREATE TABLE quiz_seen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### User Stats (XP/Streak/Level)
```sql
CREATE TABLE user_stats (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    total_xp INTEGER NOT NULL DEFAULT 0,
    current_streak INTEGER NOT NULL DEFAULT 0,
    longest_streak INTEGER NOT NULL DEFAULT 0,
    last_active_date TEXT
);
```

### Daily Activity
```sql
CREATE TABLE daily_activity (
    date TEXT PRIMARY KEY,
    xp INTEGER NOT NULL DEFAULT 0,
    lessons INTEGER NOT NULL DEFAULT 0,
    quizzes INTEGER NOT NULL DEFAULT 0
);
```

## XP Values

| Event | XP | Streak |
|-------|----|--------|
| Lesson completed | +15 | Updated |
| Quiz answer correct | +5 | Updated |
| Quiz answer wrong | 0 | Updated (streak maintained) |
| Daily goal | 50 XP | — |

## Levels (10 total)

| Level | XP Required |
|-------|-------------|
| 1 | 0 |
| 2 | 50 |
| 3 | 120 |
| 4 | 220 |
| 5 | 360 |
| 6 | 550 |
| 7 | 800 |
| 8 | 1100 |
| 9 | 1500 |
| 10 | 2000+ (max) |
