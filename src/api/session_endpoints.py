from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from src.services.session_manager import session_manager
from typing import Dict, Optional

router = APIRouter()

class CreateSessionRequest(BaseModel):
    user_id: str
    quiz_id: str

class UpdateProgressRequest(BaseModel):
    question_id: int
    answer: str

@router.post("/", response_model=dict)
async def create_session(request: CreateSessionRequest):
    """Create a new quize session"""
    attempt = await session_manager.create_session(
        request.user_id,
        request.quiz_id
    )

    return {
        "id": attempt.id,
        "user_id": attempt.user_id,
        "quiz_id": attempt.quiz_id,
        "status": attempt.status.value,
        "time_remaining": attempt.time_remaining
    }


@router.put("/{session_id}/progress")
async def update_progress(session_id: str, request: UpdateProgressRequest):
    """Update quiz progress"""
    success = await session_manager.update_progress(
        session_id,
        request.question_id,
        request.answer
    )

    if not success:
        raise HTTPException(
            status_code=409,
            detail="Update conflict - session may have been modified"
        )

    return {"message": "Progress updated successfully"}
