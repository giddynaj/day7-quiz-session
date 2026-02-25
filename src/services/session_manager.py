from src.models.attempt import QuizAttempt, AttemptStatus
from src.services.database import get_db
import uuid
from datetime import datetime, timedelta
from typing import Optional, List
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

class SessionManager:
    def __init__(self):
        self.auto_save_tasks = {}

    async def create_session(self, user_id: str, quiz_id: str) -> QuizAttempt:
        """ Create a new quiz attempt session"""
        attempt = QuizAttempt(
            id=str(uuid.uuid4()),
            user_id=user_id,
            quiz_id=quiz_id,
            started_at=datetime.timezone.utc()
        )

        db = await get_db()
