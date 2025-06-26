"""
Service for managing user assessments (listing, starting, resuming, submitting)
"""

import uuid
from app.models.launchpad.hra import HraStep, Question
from sanic import Sanic
from sanic.log import logger
from typing import Optional, List, Dict, Any
from datetime import datetime
from pymongo import ASCENDING

class AssessmentServiceException(Exception):
    pass

class AssessmentService:
    def __init__(self, app: Sanic):
        self.app = app
        self.collection = app.ctx.mongo['launchpad_db']['assessments']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['assessments']
            try:
                await collection.create_index([('user_id', ASCENDING)])
                await collection.create_index([('session_id', ASCENDING)], unique=True)
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def list_assessments(self, user_id: str) -> List[Dict[str, Any]]:
        """Return a list of assessment sessions for the user."""
        try:
            cursor = self.collection.find({"user_id": user_id})
            return [doc async for doc in cursor]
        except Exception as e:
            logger.error(f"Error listing assessments for {user_id}: {e}")
            raise AssessmentServiceException("Failed to list assessments")

    async def start_assessment(self, user_id: str, template: Dict[str, Any]) -> str:
        """Start a new assessment session for the user, based on a template (dict with steps/questions). Returns session_id."""
        try:
            session_id = str(uuid.uuid4())
            assessment_doc = {
                "session_id": session_id,
                "user_id": user_id,
                "template": template,  # Should be validated/structured as needed
                "responses": {},
                "status": "in_progress",
                "started_at": datetime.utcnow().isoformat(),
                "completed_at": None
            }
            await self.collection.insert_one(assessment_doc)
            return session_id
        except Exception as e:
            logger.error(f"Error starting assessment for {user_id}: {e}")
            raise AssessmentServiceException("Failed to start assessment")

    async def resume_assessment(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Resume an in-progress assessment session."""
        try:
            doc = await self.collection.find_one({"user_id": user_id, "session_id": session_id, "status": "in_progress"})
            return doc
        except Exception as e:
            logger.error(f"Error resuming assessment for {user_id}: {e}")
            raise AssessmentServiceException("Failed to resume assessment")

    async def submit_assessment(self, user_id: str, session_id: str, answers: Dict[str, Any]) -> bool:
        """Submit answers for an assessment session. Marks as completed."""
        try:
            result = await self.collection.update_one(
                {"user_id": user_id, "session_id": session_id, "status": "in_progress"},
                {"$set": {"responses": answers, "status": "completed", "completed_at": datetime.utcnow().isoformat()}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error submitting assessment for {user_id}: {e}")
            raise AssessmentServiceException("Failed to submit assessment")

    async def get_assessment_result(self, user_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        """Get the result/score for a completed assessment session."""
        try:
            doc = await self.collection.find_one({"user_id": user_id, "session_id": session_id, "status": "completed"})
            if not doc:
                return None
            # Here you could add logic to calculate a score/result based on responses
            return doc.get("responses", {})
        except Exception as e:
            logger.error(f"Error getting assessment result for {user_id}: {e}")
            raise AssessmentServiceException("Failed to get assessment result") 