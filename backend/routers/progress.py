from fastapi import APIRouter, Request
from pydantic import BaseModel
from models.database import get_connection
router = APIRouter()

class MarkLearned(BaseModel):
    topic_id: str

@router.get("")
async def get_progress(request: Request):
    kb = request.app.state.kb
    conn = get_connection()
    learned = conn.execute("SELECT COUNT(*) as c FROM progress").fetchone()["c"]
    conn.close()
    return {"total_topics": kb.topic_count, "learned": learned, "percentage": round(learned/kb.topic_count*100, 1) if kb.topic_count else 0}

@router.post("/mark")
async def mark_learned(body: MarkLearned):
    conn = get_connection()
    conn.execute("INSERT OR IGNORE INTO progress (topic_id) VALUES (?)", (body.topic_id,))
    conn.commit()
    conn.close()
    return {"status": "marked"}
