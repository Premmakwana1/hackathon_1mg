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