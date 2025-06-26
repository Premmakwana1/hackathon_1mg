"""
Service for managing user challenges (listing, joining, progress, check-in)
"""

import uuid
from sanic import Sanic
from sanic.log import logger
from typing import Optional, List, Dict, Any
from datetime import datetime
from pymongo import ASCENDING

class ChallengeServiceException(Exception):
    pass

class ChallengeService:
    def __init__(self, app: Sanic):
        self.app = app
        self.challenges = app.ctx.mongo['launchpad_db']['challenges']
        self.user_challenges = app.ctx.mongo['launchpad_db']['user_challenges']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            challenges = app.ctx.mongo['launchpad_db']['challenges']
            user_challenges = app.ctx.mongo['launchpad_db']['user_challenges']
            try:
                await challenges.create_index([('challenge_id', ASCENDING)], unique=True)
                await user_challenges.create_index([('user_id', ASCENDING)])
                await user_challenges.create_index([('challenge_id', ASCENDING)])
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def list_challenges(self, user_id: str) -> List[Dict[str, Any]]:
        """Return a list of all challenges, with user participation status."""
        try:
            challenges = [doc async for doc in self.challenges.find({})]
            user_chal_ids = set()
            async for uc in self.user_challenges.find({"user_id": user_id}):
                user_chal_ids.add(uc["challenge_id"])
            for c in challenges:
                c["joined"] = c.get("challenge_id") in user_chal_ids
            return challenges
        except Exception as e:
            logger.error(f"Error listing challenges for {user_id}: {e}")
            raise ChallengeServiceException("Failed to list challenges")

    async def join_challenge(self, user_id: str, challenge_id: str) -> str:
        """Add the user to a challenge. Returns user_challenge_id."""
        try:
            # Check if already joined
            existing = await self.user_challenges.find_one({"user_id": user_id, "challenge_id": challenge_id})
            if existing:
                return existing["user_challenge_id"]
            user_challenge_id = str(uuid.uuid4())
            doc = {
                "user_challenge_id": user_challenge_id,
                "user_id": user_id,
                "challenge_id": challenge_id,
                "status": "in_progress",
                "progress": 0,
                "check_ins": [],
                "joined_at": datetime.utcnow().isoformat(),
                "completed_at": None
            }
            await self.user_challenges.insert_one(doc)
            return user_challenge_id
        except Exception as e:
            logger.error(f"Error joining challenge for {user_id}: {e}")
            raise ChallengeServiceException("Failed to join challenge")

    async def check_in(self, user_id: str, challenge_id: str) -> bool:
        """Mark a check-in for the user in a challenge."""
        try:
            now = datetime.utcnow().isoformat()
            result = await self.user_challenges.update_one(
                {"user_id": user_id, "challenge_id": challenge_id, "status": "in_progress"},
                {"$push": {"check_ins": now}, "$inc": {"progress": 1}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error check-in for {user_id} in challenge {challenge_id}: {e}")
            raise ChallengeServiceException("Failed to check-in")

    async def get_user_challenges(self, user_id: str) -> List[Dict[str, Any]]:
        """List all challenges the user has joined, with progress."""
        try:
            return [doc async for doc in self.user_challenges.find({"user_id": user_id})]
        except Exception as e:
            logger.error(f"Error getting user challenges for {user_id}: {e}")
            raise ChallengeServiceException("Failed to get user challenges")

    async def leave_challenge(self, user_id: str, challenge_id: str) -> bool:
        """Allow user to leave a challenge (delete user_challenge entry)."""
        try:
            result = await self.user_challenges.delete_one({"user_id": user_id, "challenge_id": challenge_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error leaving challenge for {user_id}: {e}")
            raise ChallengeServiceException("Failed to leave challenge")

    async def get_challenge_progress(self, user_id: str, challenge_id: str) -> Dict[str, Any]:
        """Return progress, check-ins, total checkpoints, completion percent, and challenge details for a user's challenge."""
        try:
            user_chal = await self.user_challenges.find_one({"user_id": user_id, "challenge_id": challenge_id})
            chal = await self.challenges.find_one({"challenge_id": challenge_id})
            if not user_chal or not chal:
                return {}
            check_ins = user_chal.get("check_ins", [])
            total_checkpoints = chal.get("duration", len(check_ins))
            progress = len(check_ins)
            completion_percent = int((progress / total_checkpoints) * 100) if total_checkpoints else 0
            return {
                "challenge_id": challenge_id,
                "title": chal.get("title"),
                "description": chal.get("description"),
                "tags": chal.get("tags", []),
                "duration": total_checkpoints,
                "check_ins": check_ins,
                "progress": progress,
                "completion_percent": completion_percent,
                "status": user_chal.get("status", "in_progress"),
            }
        except Exception as e:
            logger.error(f"Error getting challenge progress for {user_id}, {challenge_id}: {e}")
            raise ChallengeServiceException("Failed to get challenge progress")

    async def get_user_challenges_by_status(self, user_id: str, status: str) -> List[Dict[str, Any]]:
        """List user challenges filtered by status (e.g., in_progress, completed)."""
        try:
            return [doc async for doc in self.user_challenges.find({"user_id": user_id, "status": status})]
        except Exception as e:
            logger.error(f"Error getting user challenges by status for {user_id}: {e}")
            raise ChallengeServiceException("Failed to get user challenges by status")

    async def get_challenge_details(self, challenge_id: str) -> Dict[str, Any]:
        """Fetch all details for a specific challenge."""
        try:
            chal = await self.challenges.find_one({"challenge_id": challenge_id})
            return chal if chal else {}
        except Exception as e:
            logger.error(f"Error getting challenge details for {challenge_id}: {e}")
            raise ChallengeServiceException("Failed to get challenge details") 