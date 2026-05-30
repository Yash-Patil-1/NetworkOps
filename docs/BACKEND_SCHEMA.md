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

## SQLite (User State)
```sql
CREATE TABLE progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL UNIQUE,
    learned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question_id TEXT NOT NULL,
    topic_id TEXT NOT NULL,
    correct INTEGER NOT NULL,
    user_answer TEXT,
    answered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE quiz_seen (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    seen_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```
