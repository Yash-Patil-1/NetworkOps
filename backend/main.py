"""
NetworkOps — Network Operations Learning Platform
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routers import topics, quiz, domains, progress, streak, lessons
from models.database import init_db
from services.knowledge_base import NetworkKnowledgeBase
from services.quiz_engine import QuizEngine


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🌐 Loading NetworkOps knowledge base...")
    app.state.kb = NetworkKnowledgeBase()
    app.state.kb.load()
    app.state.quiz_engine = QuizEngine(app.state.kb.questions)
    print(f"✅ Loaded {app.state.kb.topic_count} topics, {app.state.kb.question_count} questions")
    await init_db()
    print("✅ Database initialized.")
    yield


app = FastAPI(title="NetworkOps", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

app.include_router(topics.router, prefix="/api/topics", tags=["Topics"])
app.include_router(quiz.router, prefix="/api/quiz", tags=["Quiz"])
app.include_router(domains.router, prefix="/api/domains", tags=["Domains"])
app.include_router(progress.router, prefix="/api/progress", tags=["Progress"])
app.include_router(streak.router, prefix="/api/streak", tags=["Streak"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])


@app.get("/")
async def root():
    return {"name": "NetworkOps", "version": "1.0.0", "author": "Yash Patil"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
