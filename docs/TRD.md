# Technical Requirements Document (TRD)
## NetworkOps — Network Operations Learning Platform

---

## 1. Architecture

Same proven stack as VAPTLearn/GRCLearn + Quiz Engine:

```
┌─────────────────────────────────────────────────────┐
│           Frontend (React + Vite + Tailwind v4)     │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │  Theory  │ │   Quiz   │ │  Protocol         │   │
│  │  Reader  │ │  Engine  │ │  Explorer         │   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │ REST API
┌─────────────────────▼───────────────────────────────┐
│              Backend (FastAPI)                        │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │Knowledge │ │  Quiz    │ │  Progress         │   │
│  │  Base    │ │  Engine  │ │  Tracker          │   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
└─────────────────────┬───────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────┐
│              Data Layer                              │
│  ┌──────────┐ ┌──────────┐ ┌───────────────────┐   │
│  │  JSON    │ │  SQLite  │ │  Quiz State       │   │
│  │(topics)  │ │(progress)│ │  (seen queue)     │   │
│  └──────────┘ └──────────┘ └───────────────────┘   │
└─────────────────────────────────────────────────────┘
```

---

## 2. Technology Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, Tailwind v4 (Hyperstudio), React Router |
| Backend | FastAPI, Python 3.10+, Uvicorn, Pydantic |
| Data | JSON (topics, questions), SQLite (user state) |
| Search | Fuse.js (client-side) |

---

## 3. Design System

Same Hyperstudio theme (monochrome + amber) for portfolio cohesion across all 3 platforms.

---

## 4. API Specification

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/topics` | List topics (filter by domain, phase) |
| GET | `/api/topics/{id}` | Topic detail with theory |
| GET | `/api/topics/search?q=` | Search topics |
| GET | `/api/domains` | List all domains |
| GET | `/api/phases` | Learning phases |
| GET | `/api/quiz/next?topic={id}` | Get next quiz question (respects repetition) |
| POST | `/api/quiz/answer` | Submit answer, get validation |
| GET | `/api/quiz/stats` | Quiz performance stats |
| GET | `/api/progress` | User progress |
| POST | `/api/progress/mark` | Mark topic learned |
| GET | `/api/protocols` | List protocols |
| GET | `/api/protocols/{name}` | Protocol detail |

---

## 5. Quiz Engine Logic

```python
class QuizEngine:
    def get_next_question(self, topic_id: str, user_seen: list[str]) -> dict:
        """
        Get next question respecting repetition rules:
        - Filter out questions seen in last 80 attempts for this topic
        - Pick randomly from remaining
        """
        all_questions = self.get_questions_for_topic(topic_id)
        recent_80 = user_seen[-80:] if len(user_seen) > 80 else user_seen
        available = [q for q in all_questions if q["id"] not in recent_80]
        if not available:
            available = all_questions  # Reset if all seen
        return random.choice(available)

    def validate_answer(self, question: dict, user_answer: str) -> dict:
        """
        Validate answer based on question type:
        - theory: exact match or contains keywords
        - command: check required_keywords present
        - scenario: check against correct_answers list
        """
        ...
```

---

## 6. Topic Schema

```json
{
  "id": "ospf-fundamentals",
  "domain": "network_engineering",
  "phase": 2,
  "name": "OSPF Fundamentals",
  "theory": {
    "what": "Open Shortest Path First — a link-state routing protocol...",
    "why": "OSPF is the most widely used IGP in enterprise networks because...",
    "how": "OSPF works by building a Link-State Database (LSDB) through...",
    "when": "Use OSPF when you need fast convergence, scalability, and...",
    "key_concepts": ["LSA types", "Areas", "DR/BDR", "SPF algorithm"],
    "configuration": "router ospf 1\n network 10.0.0.0 0.0.0.255 area 0",
    "troubleshooting": ["show ip ospf neighbor", "show ip ospf database", "debug ip ospf adj"]
  },
  "examples": [...],
  "quiz_questions": [...],
  "related_topics": ["bgp-fundamentals", "routing-basics"],
  "difficulty": "intermediate",
  "tags": ["routing", "igp", "link-state"]
}
```

---

## 7. File Structure

```
NetworkOps/
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── routers/
│   │   ├── topics.py
│   │   ├── quiz.py
│   │   ├── domains.py
│   │   ├── protocols.py
│   │   └── progress.py
│   ├── services/
│   │   ├── knowledge_base.py
│   │   └── quiz_engine.py
│   ├── models/
│   │   ├── database.py
│   │   └── schemas.py
│   ├── data/
│   │   ├── topics/
│   │   │   ├── fundamentals.json
│   │   │   ├── engineering.json
│   │   │   ├── noc.json
│   │   │   ├── security.json
│   │   │   ├── cloud.json
│   │   │   └── automation.json
│   │   ├── questions/
│   │   │   ├── fundamentals_quiz.json
│   │   │   ├── engineering_quiz.json
│   │   │   └── ...
│   │   ├── protocols.json
│   │   ├── domains.json
│   │   └── phases.json
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Topics.jsx
│   │   │   ├── TopicDetail.jsx
│   │   │   ├── Quiz.jsx
│   │   │   ├── Protocols.jsx
│   │   │   └── Progress.jsx
│   │   └── components/
│   └── ...
├── docs/
├── README.md
├── LICENSE
└── setup.sh
```
