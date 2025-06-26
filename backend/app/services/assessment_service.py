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
        self.templates = app.ctx.mongo['launchpad_db']['assessment_templates']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['assessments']
            templates = app.ctx.mongo['launchpad_db']['assessment_templates']
            try:
                await collection.create_index([('user_id', ASCENDING)])
                await collection.create_index([('session_id', ASCENDING)], unique=True)
                await templates.create_index([('template_id', ASCENDING)], unique=True)
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
        """Get the result/score for a completed assessment session, with improvement tips."""
        try:
            doc = await self.collection.find_one({"user_id": user_id, "session_id": session_id, "status": "completed"})
            if not doc:
                return None
            responses = doc.get("responses", {})
            # Example scoring: count non-empty answers
            score = sum(1 for v in responses.values() if v)
            total = len(responses)
            percent = int((score / total) * 100) if total else 0
            # Example improvement tips (static or dynamic)
            tips = [
                "Don't worry it will take daily 25 minutes effort",
                "You need to closely monitor on your food choices",
                "Addition of sport in your daily routine can really help",
                "Make sure you are drinking enough water"
            ]
            return {
                "score": score,
                "out_of": total,
                "percent": percent,
                "tips": tips,
                "responses": responses
            }
        except Exception as e:
            logger.error(f"Error getting assessment result for {user_id}: {e}")
            raise AssessmentServiceException("Failed to get assessment result")

    async def list_templates(self) -> List[Dict[str, Any]]:
        """Return a list of available assessment templates."""
        try:
            return [doc async for doc in self.templates.find({})]
        except Exception as e:
            logger.error(f"Error listing assessment templates: {e}")
            raise AssessmentServiceException("Failed to list templates")

    async def get_template_details(self, template_id: str) -> Dict[str, Any]:
        """Fetch all details for a specific assessment template."""
        try:
            doc = await self.templates.find_one({"template_id": template_id})
            return doc if doc else {}
        except Exception as e:
            logger.error(f"Error getting template details for {template_id}: {e}")
            raise AssessmentServiceException("Failed to get template details")

    async def get_assessment_progress(self, user_id: str, session_id: str) -> Dict[str, Any]:
        """Return percent complete and current question for an in-progress assessment."""
        try:
            doc = await self.collection.find_one({"user_id": user_id, "session_id": session_id})
            if not doc:
                return {}
            template = doc.get("template", {})
            steps = template.get("steps", [])
            responses = doc.get("responses", {})
            total = len(steps)
            answered = len(responses)
            percent_complete = int((answered / total) * 100) if total else 0
            current_question = steps[answered] if answered < total else None
            return {
                "percent_complete": percent_complete,
                "current_question": current_question,
                "total_questions": total,
                "answered": answered
            }
        except Exception as e:
            logger.error(f"Error getting assessment progress for {user_id}, {session_id}: {e}")
            raise AssessmentServiceException("Failed to get assessment progress")

    async def list_assessments_by_status(self, user_id: str, status: str) -> List[Dict[str, Any]]:
        """Return a list of assessment sessions for the user filtered by status."""
        try:
            cursor = self.collection.find({"user_id": user_id, "status": status})
            return [doc async for doc in cursor]
        except Exception as e:
            logger.error(f"Error listing assessments by status for {user_id}: {e}")
            raise AssessmentServiceException("Failed to list assessments by status") 