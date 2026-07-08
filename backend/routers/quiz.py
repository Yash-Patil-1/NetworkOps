from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
from models.database import get_connection
from services.stats import award_xp, record_activity, XP_QUIZ_CORRECT

router = APIRouter()

class AnswerSubmit(BaseModel):
    question_id: str
    topic_id: str
    answer: str

@router.get("/next")
async def get_next_question(request: Request, topic: str):
    """Get next quiz question for a topic (respects repetition rules)."""
    conn = get_connection()
    rows = conn.execute("SELECT question_id FROM quiz_seen WHERE topic_id = ? ORDER BY seen_at DESC", (topic,)).fetchall()
    seen_ids = [r["question_id"] for r in rows]
    conn.close()

    question = request.app.state.quiz_engine.get_next_question(topic, seen_ids)
    if not question:
        raise HTTPException(404, "No questions available for this topic")

    # Record as seen
    conn = get_connection()
    conn.execute("INSERT INTO quiz_seen (topic_id, question_id) VALUES (?, ?)", (topic, question["id"]))
    conn.commit()
    conn.close()

    # Return without correct answers (don't leak)
    return {
        "id": question["id"],
        "topic_id": question["topic_id"],
        "type": question["type"],
        "difficulty": question["difficulty"],
        "question": question["question"],
        "hints": question.get("hints", []),
    }

@router.post("/answer")
async def submit_answer(request: Request, body: AnswerSubmit):
    """Submit answer and get validation result."""
    # Find the question
    questions = request.app.state.kb.get_questions_for_topic(body.topic_id)
    question = next((q for q in questions if q["id"] == body.question_id), None)
    if not question:
        raise HTTPException(404, "Question not found")

    result = request.app.state.quiz_engine.validate_answer(question, body.answer)

    # Record in history
    conn = get_connection()
    conn.execute(
        "INSERT INTO quiz_history (question_id, topic_id, correct, user_answer) VALUES (?, ?, ?, ?)",
        (body.question_id, body.topic_id, 1 if result["correct"] else 0, body.answer)
    )
    conn.commit()
    conn.close()

    # Award XP for correct answers; maintain streak for any attempt
    if result["correct"]:
        streak_data = award_xp(XP_QUIZ_CORRECT, "quiz")
        result["xp_awarded"] = XP_QUIZ_CORRECT
    else:
        streak_data = record_activity("quiz")
        result["xp_awarded"] = 0
    result["current_streak"] = streak_data["current_streak"]
    result["total_xp"] = streak_data["total_xp"]

    return result

@router.get("/stats")
async def get_quiz_stats(request: Request, topic: str = None):
    """Get quiz performance stats."""
    conn = get_connection()
    if topic:
        total = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE topic_id = ?", (topic,)).fetchone()["c"]
        correct = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE topic_id = ? AND correct = 1", (topic,)).fetchone()["c"]
    else:
        total = conn.execute("SELECT COUNT(*) as c FROM quiz_history").fetchone()["c"]
        correct = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE correct = 1").fetchone()["c"]
    conn.close()
    return {"total_answered": total, "correct": correct, "accuracy": round(correct/total*100, 1) if total else 0}


@router.get("/stats")
async def get_quiz_stats(request: Request, topic: str = None):
    """Get quiz performance stats."""
    conn = get_connection()
    if topic:
        total = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE topic_id = ?", (topic,)).fetchone()["c"]
        correct = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE topic_id = ? AND correct = 1", (topic,)).fetchone()["c"]
    else:
        total = conn.execute("SELECT COUNT(*) as c FROM quiz_history").fetchone()["c"]
        correct = conn.execute("SELECT COUNT(*) as c FROM quiz_history WHERE correct = 1").fetchone()["c"]
    conn.close()
    return {"total_answered": total, "correct": correct, "accuracy": round(correct/total*100, 1) if total else 0}
