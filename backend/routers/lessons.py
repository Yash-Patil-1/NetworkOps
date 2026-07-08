"""Guided lessons router for NetworkOps — wraps topic theory + quiz checkpoints."""

from fastapi import APIRouter, Request, HTTPException
from services.stats import award_xp, XP_LESSON_COMPLETE

router = APIRouter()

# NetworkOps topics map 1:1 to question topic_ids, so we can derive checkpoints at runtime
# This dict maps lesson (topic) IDs to their question topic IDs — typically the same, but
# allows manual overrides when topic_id differs from the lesson id.
# Left empty — the router automatically checks self-id at runtime.
LESSON_QUESTION_TOPICS: dict[str, list[str]] = {}


def _topic_to_sections(topic: dict) -> list[dict]:
    """Convert topic theory fields into ordered lesson sections."""
    theory = topic.get("theory", {})
    sections = []

    field_map = {
        "what": "Understanding {name}",
        "why": "Why {name} Matters",
        "how": "How {name} Works",
        "when": "When to Use {name}",
    }
    name = topic.get("name", "")

    for field, title_template in field_map.items():
        content = theory.get(field)
        if content and isinstance(content, str) and len(content.strip()) > 10:
            sections.append({
                "title": title_template.format(name=name),
                "content": content,
                "field": field,
            })

    # Configuration section
    config = theory.get("configuration")
    if config and isinstance(config, str) and len(config.strip()) > 5:
        sections.append({
            "title": f"Configuration — {name}",
            "content": f"```\n{config}\n```",
            "field": "configuration",
        })

    # Troubleshooting section
    troubleshooting = theory.get("troubleshooting", [])
    if troubleshooting and len(troubleshooting) > 0:
        items = "\n".join(f"• {s}" for s in troubleshooting)
        sections.append({
            "title": f"Troubleshooting {name}",
            "content": f"Common issues and debugging commands:\n\n{items}",
            "field": "troubleshooting",
        })

    return sections


@router.get("")
async def list_lessons(request: Request):
    """List all topics as lessons with section counts and checkpoint availability."""
    kb = request.app.state.kb
    quiz_engine = request.app.state.quiz_engine
    lessons = []

    for topic in kb.topics:
        topic_id = topic["id"]
        sections = _topic_to_sections(topic)
        # Count questions available for this topic
        topic_questions = quiz_engine._by_topic.get(topic_id, [])
        lessons.append({
            "id": topic_id,
            "title": topic.get("name", ""),
            "domain": topic.get("domain", ""),
            "difficulty": topic.get("difficulty", ""),
            "section_count": len(sections),
            "checkpoint_count": len(topic_questions),
            "tags": topic.get("tags", []),
        })

    # Sort: topics with more checkpoints first (better lessons), then by name
    lessons.sort(key=lambda l: (-l["checkpoint_count"], l["title"]))

    return {"lessons": lessons, "total": len(lessons)}


@router.get("/{topic_id}")
async def get_lesson(topic_id: str, request: Request):
    """Get a lesson with ordered sections and checkpoint question info."""
    kb = request.app.state.kb
    quiz_engine = request.app.state.quiz_engine

    topic = kb.get_topic(topic_id)
    if not topic:
        raise HTTPException(404, f"Topic '{topic_id}' not found")

    sections = _topic_to_sections(topic)
    if not sections:
        raise HTTPException(404, f"Topic '{topic_id}' has no theory content")

    # Find checkpoint questions for this topic
    topic_questions = quiz_engine._by_topic.get(topic_id, [])
    checkpoint_question_ids = [q["id"] for q in topic_questions]

    return {
        "id": topic_id,
        "title": topic.get("name", ""),
        "domain": topic.get("domain", ""),
        "difficulty": topic.get("difficulty", ""),
        "sections": sections,
        "checkpoint_question_ids": checkpoint_question_ids,
        "key_concepts": topic.get("theory", {}).get("key_concepts", []),
    }


@router.post("/{topic_id}/complete")
async def complete_lesson(topic_id: str, request: Request):
    """Mark lesson as complete and award lesson XP."""
    kb = request.app.state.kb

    topic = kb.get_topic(topic_id)
    if not topic:
        raise HTTPException(404, f"Topic '{topic_id}' not found")

    # Award lesson XP
    result = award_xp(XP_LESSON_COMPLETE, "lesson")

    # Mark progress
    from models.database import get_connection
    conn = get_connection()
    conn.execute(
        "INSERT OR IGNORE INTO progress (topic_id) VALUES (?)",
        (topic_id,)
    )
    conn.commit()
    conn.close()

    return {
        "status": "completed",
        "xp_awarded": XP_LESSON_COMPLETE,
        **result,
    }
