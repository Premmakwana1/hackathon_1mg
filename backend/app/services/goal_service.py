"""
Service for user goals (setting, tracking, updating goals)
"""

import uuid
from app.models.launchpad.activity_tracker import Goals
from sanic import Sanic
from sanic.log import logger
from typing import Optional, Dict, Any
from pymongo import ASCENDING

class GoalServiceException(Exception):
    pass

class GoalService:
    def __init__(self, app: Sanic):
        self.app = app
        self.collection = app.ctx.mongo['launchpad_db']['user_goals']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['user_goals']
            try:
                await collection.create_index([('user_id', ASCENDING)], unique=True)
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def get_goals(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Return the user's goals."""
        try:
            doc = await self.collection.find_one({"user_id": user_id})
            if doc and "goals" in doc:
                return doc["goals"]
            return None
        except Exception as e:
            logger.error(f"Error getting goals for {user_id}: {e}")
            raise GoalServiceException("Failed to get goals")

    async def set_goal(self, user_id: str, goal_data: Dict[str, Any]) -> bool:
        """Set new goals for the user (overwrites existing)."""
        try:
            # Validate using Goals model
            goals = Goals(**goal_data)
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {"goals": goals.dict()}},
                upsert=True
            )
            return result.modified_count > 0 or result.upserted_id is not None
        except Exception as e:
            logger.error(f"Error setting goals for {user_id}: {e}")
            raise GoalServiceException("Failed to set goals")

    async def update_goal(self, user_id: str, goal_type: str, goal_data: Dict[str, Any]) -> bool:
        """Update a specific goal (goal_type: 'daily' or 'weekly')."""
        try:
            # Validate partial update using Goals model
            if goal_type not in ['daily', 'weekly']:
                raise ValueError("goal_type must be 'daily' or 'weekly'")
            update_field = f"goals.{goal_type}"
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$set": {update_field: goal_data}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating {goal_type} goal for {user_id}: {e}")
            raise GoalServiceException("Failed to update goal")

    async def delete_goal(self, user_id: str, goal_type: str) -> bool:
        """Delete a specific goal (goal_type: 'daily' or 'weekly')."""
        try:
            if goal_type not in ['daily', 'weekly']:
                raise ValueError("goal_type must be 'daily' or 'weekly'")
            update_field = f"goals.{goal_type}"
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$unset": {update_field: ""}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting {goal_type} goal for {user_id}: {e}")
            raise GoalServiceException("Failed to delete goal") 