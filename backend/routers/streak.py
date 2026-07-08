"""Streak and XP endpoints for NetworkOps."""

from fastapi import APIRouter
from services.stats import get_streak

router = APIRouter()


@router.get("")
async def streak():
    """Get current streak, XP, level, and daily activity data."""
    return get_streak()
