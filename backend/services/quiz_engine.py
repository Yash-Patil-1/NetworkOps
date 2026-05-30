"""
Quiz Engine — intelligent question selection with low repetition.
Supports command-type, scenario, theory, and troubleshooting questions.
"""

import random
import re
from typing import Optional


class QuizEngine:
    """Manages quiz question selection and answer validation."""

    def __init__(self, questions: list[dict]):
        self.questions = questions
        self._by_topic: dict[str, list[dict]] = {}
        for q in questions:
            topic = q.get("topic_id", "general")
            if topic not in self._by_topic:
                self._by_topic[topic] = []
            self._by_topic[topic].append(q)

    def get_next_question(self, topic_id: str, seen_ids: list[str]) -> Optional[dict]:
        """
        Get next question respecting repetition rules:
        - Filter out questions seen in last 80 attempts for this topic
        - Pick randomly from remaining
        - If all seen, reset (allow any)
        """
        topic_questions = self._by_topic.get(topic_id, [])
        if not topic_questions:
            return None

        # Only exclude last 80 seen
        recent_seen = set(seen_ids[-80:]) if len(seen_ids) > 80 else set(seen_ids)
        available = [q for q in topic_questions if q["id"] not in recent_seen]

        if not available:
            # All questions seen recently — allow any
            available = topic_questions

        return random.choice(available)

    def validate_answer(self, question: dict, user_answer: str) -> dict:
        """
        Validate user's answer based on question type and validation rules.
        Returns: {"correct": bool, "explanation": str, "expected": str}
        """
        user_answer = user_answer.strip()
        correct_answers = question.get("correct_answers", [])
        validation_type = question.get("validation_type", "contains_any")
        required_keywords = question.get("required_keywords", [])

        is_correct = False

        if validation_type == "exact":
            # Exact match (case-insensitive)
            is_correct = user_answer.lower() in [a.lower() for a in correct_answers]

        elif validation_type == "contains_all":
            # Must contain all required keywords
            answer_lower = user_answer.lower()
            is_correct = all(kw.lower() in answer_lower for kw in required_keywords)

        elif validation_type == "contains_any":
            # Must match any correct answer (fuzzy)
            answer_lower = user_answer.lower()
            for correct in correct_answers:
                if self._fuzzy_match(answer_lower, correct.lower()):
                    is_correct = True
                    break

        return {
            "correct": is_correct,
            "explanation": question.get("explanation", ""),
            "expected": correct_answers[0] if correct_answers else "",
            "user_answer": user_answer,
        }

    def get_topic_stats(self, topic_id: str) -> dict:
        """Get question count for a topic."""
        questions = self._by_topic.get(topic_id, [])
        return {
            "total_questions": len(questions),
            "by_type": self._count_by_type(questions),
            "by_difficulty": self._count_by_difficulty(questions),
        }

    def _fuzzy_match(self, user: str, correct: str) -> bool:
        """Simple fuzzy matching — checks if key parts of correct answer are in user's answer."""
        # Remove extra whitespace and normalize
        user_clean = re.sub(r'\s+', ' ', user).strip()
        correct_clean = re.sub(r'\s+', ' ', correct).strip()

        # Direct match
        if user_clean == correct_clean:
            return True

        # Check if user answer contains the core of correct answer
        # Split correct into words, check if 70%+ are present
        correct_words = set(correct_clean.split())
        if not correct_words:
            return False
        user_words = set(user_clean.split())
        overlap = len(correct_words & user_words) / len(correct_words)
        return overlap >= 0.7

    def _count_by_type(self, questions: list[dict]) -> dict:
        counts = {}
        for q in questions:
            t = q.get("type", "theory")
            counts[t] = counts.get(t, 0) + 1
        return counts

    def _count_by_difficulty(self, questions: list[dict]) -> dict:
        counts = {}
        for q in questions:
            d = q.get("difficulty", "medium")
            counts[d] = counts.get(d, 0) + 1
        return counts
