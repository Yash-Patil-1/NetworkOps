from fastapi import APIRouter, Request, HTTPException, Query
from typing import Optional
router = APIRouter()

@router.get("")
async def list_topics(request: Request, domain: Optional[str] = None, phase: Optional[int] = None, limit: int = Query(50, le=500), offset: int = 0):
    kb = request.app.state.kb
    results = kb.filter_topics(domain=domain, phase=phase)
    return {"topics": results[offset:offset+limit], "total": len(results)}

@router.get("/search")
async def search_topics(request: Request, q: str = ""):
    if len(q) < 2: return {"topics": [], "total": 0}
    results = request.app.state.kb.search_topics(q)
    return {"topics": results[:50], "total": len(results)}

@router.get("/{topic_id}")
async def get_topic(request: Request, topic_id: str):
    topic = request.app.state.kb.get_topic(topic_id)
    if not topic: raise HTTPException(404, "Topic not found")
    return topic
