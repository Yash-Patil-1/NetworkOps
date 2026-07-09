"""NetworkOps Knowledge Base — loads topics, questions."""

import json
from pathlib import Path
from typing import Optional

DATA_DIR = Path(__file__).parent.parent / "data"


class NetworkKnowledgeBase:
    def __init__(self):
        self.topics: list[dict] = []
        self.questions: list[dict] = []
        self.domains: list[dict] = []
        self._topic_index: dict[str, dict] = {}

    def load(self):
        # Load topics
        topics_dir = DATA_DIR / "topics"
        if topics_dir.exists():
            for f in sorted(topics_dir.glob("*.json")):
                with open(f, 'r') as fp:
                    self.topics.extend(json.load(fp))
        self._topic_index = {t["id"]: t for t in self.topics}

        # Load questions
        questions_dir = DATA_DIR / "questions"
        if questions_dir.exists():
            for f in sorted(questions_dir.glob("*.json")):
                with open(f, 'r') as fp:
                    self.questions.extend(json.load(fp))

        # Load domains
        domains_file = DATA_DIR / "domains.json"
        if domains_file.exists():
            with open(domains_file, 'r') as f:
                self.domains = json.load(f)

    @property
    def topic_count(self) -> int:
        return len(self.topics)

    @property
    def question_count(self) -> int:
        return len(self.questions)

    def get_topic(self, topic_id: str) -> Optional[dict]:
        return self._topic_index.get(topic_id)

    def search_topics(self, query: str) -> list[dict]:
        q = query.lower()
        return [t for t in self.topics if
                q in t.get("name", "").lower() or
                q in t.get("domain", "").lower() or
                any(q in tag for tag in t.get("tags", []))]

    def filter_topics(self, domain: Optional[str] = None, phase: Optional[int] = None) -> list[dict]:
        results = self.topics
        if domain:
            results = [t for t in results if t.get("domain") == domain]
        if phase is not None:
            results = [t for t in results if t.get("phase") == phase]
        return results

    def get_questions_for_topic(self, topic_id: str) -> list[dict]:
        return [q for q in self.questions if q.get("topic_id") == topic_id]
