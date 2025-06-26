"""
Service for profile management (view/update profile, etc.)
"""

import uuid
from datetime import datetime
from app.models.launchpad.profile import ProfileStep
from sanic import Sanic
from sanic.log import logger
from typing import Optional, Dict, Any, List
from pymongo import ASCENDING
from pydantic import BaseModel
from app.db.config import DB_NAME

class ProfilePayload(BaseModel):
    steps: List[ProfileStep]

class ProfileServiceException(Exception):
    pass

class ProfileService:
    def __init__(self, app: Sanic, collection=None):
        self.app = app
        if collection is not None:
            self.collection = collection
        else:
            self.collection = app.ctx.mongo['launchpad_db']['user_profiles']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['user_profiles']
            try:
                await collection.create_index([('user_id', ASCENDING)], unique=True)
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def get_profile(self, user_id: str) -> Dict[str, Any]:
        """Return the user's profile, always as a dict with steps and completion_percent."""
        try:
            doc = await self.collection.find_one({"user_id": user_id})
            steps = doc["profile"]["steps"] if doc and "profile" in doc and "steps" in doc["profile"] else []
            # Compute completion percent (e.g., percent of steps with all userResponses filled)
            if steps:
                total = len(steps)
                completed = sum(1 for s in steps if s.userResponses and all(v is not None for v in s.userResponses.values()))
                completion_percent = int((completed / total) * 100)
            else:
                completion_percent = 0
            return {"steps": steps, "completion_percent": completion_percent}
        except Exception as e:
            logger.error(f"Error getting profile for {user_id}: {e}")
            raise ProfileServiceException("Failed to get profile")

    async def update_profile(self, user_id: str, profile_data: Dict[str, Any]) -> bool:
        """Overwrite the user's profile (validates full payload)."""
        try:
            if "steps" not in profile_data or not isinstance(profile_data["steps"], list):
                raise ValueError("Profile data must include a 'steps' list.")
            payload = ProfilePayload(**profile_data)
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"profile": payload.dict(), "updated_at": datetime.utcnow()}},
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            logger.error(f"Error updating profile for {user_id}: {e}")
            raise ProfileServiceException("Failed to update profile")

    async def patch_profile(self, user_id: str, patch_data: Dict[str, Any]) -> bool:
        """Patch the user's profile (merges new fields)."""
        try:
            doc = await self.collection.find_one({"user_id": user_id})
            if not doc or "profile" not in doc:
                raise ProfileServiceException("Profile not found for patching")
            profile = doc["profile"]
            # Merge patch_data into profile
            for k, v in patch_data.items():
                if k == "steps" and isinstance(v, list):
                    profile["steps"] = v  # Replace steps array
                else:
                    profile[k] = v
            payload = ProfilePayload(**profile)
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"profile": payload.dict(), "updated_at": datetime.utcnow()}},
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error patching profile for {user_id}: {e}")
            raise ProfileServiceException("Failed to patch profile")

    async def delete_profile(self, user_id: str) -> bool:
        """Delete the user's profile."""
        try:
            result = await self.collection.delete_one({"user_id": user_id})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting profile for {user_id}: {e}")
            raise ProfileServiceException("Failed to delete profile")

    async def get_profile_step(self, user_id: str, step: int):
        doc = await self.collection.find_one({"user_id": user_id})
        if not doc or "profile" not in doc or "steps" not in doc["profile"]:
            return None
        steps = doc["profile"]["steps"]
        for s in steps:
            if s["step"] == step:
                return s
        return None

    async def save_profile_step(self, user_id: str, step: int, step_data: dict):
        # Validate step_data using ProfileStep
        step_obj = ProfileStep(**step_data)
        doc = await self.collection.find_one({"user_id": user_id})
        if not doc or "profile" not in doc or "steps" not in doc["profile"]:
            # Create new profile with this step
            profile = {"steps": [step_obj.dict()]}
            await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"profile": profile}},
                upsert=True
            )
            return {"success": True, "nextStep": step + 1}
        # Update or add the step
        steps = doc["profile"]["steps"]
        updated = False
        for idx, s in enumerate(steps):
            if s["step"] == step:
                steps[idx] = step_obj.dict()
                updated = True
                break
        if not updated:
            steps.append(step_obj.dict())
        await self.collection.update_one(
            {"user_id": user_id},
            {"$set": {"profile.steps": steps}}
        )
        return {"success": True, "nextStep": step + 1} 