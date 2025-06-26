"""
Service for overall wellness logic (aggregates trackers, provides recommendations, etc.)
"""

from app.models.launchpad.wellness import Wellness
from sanic import Sanic
from sanic.log import logger
from typing import Optional, Dict, Any
from pymongo import ASCENDING
from pydantic import ValidationError

class WellnessServiceException(Exception):
    pass

class WellnessService:
    def __init__(self, app: Sanic, collection=None):
        self.app = app
        if collection is not None:
            self.collection = collection
        else:
            self.collection = app.ctx.mongo['launchpad_db']['wellness_configs']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['wellness_configs']
            try:
                await collection.create_index([('user_id', ASCENDING)])
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def get_wellness_data(self, user_id: str) -> Dict[str, Any]:
        """Return both wellness overview and recommendations for the user, validated and with defaults."""
        try:
            doc = await self.collection.find_one({"user_id": user_id})
            if not doc:
                # Return a default shape if no data exists
                return {
                    "wellness": {},
                    "recommendations": []
                }
            try:
                obj = Wellness(**doc.get("wellness", {})) if "wellness" in doc else None
                wellness_data = obj.dict() if obj else {}
            except ValidationError as ve:
                logger.error(f"Wellness model validation error: {ve}")
                wellness_data = {}
            recommendations = doc.get("recommendations", [])
            return {
                "wellness": wellness_data,
                "recommendations": recommendations
            }
        except (TypeError, ValueError) as e:
            logger.error(f"Invalid input for user_id {user_id}: {e}")
            raise WellnessServiceException("Invalid user_id or data format")
        except Exception as e:
            logger.error(f"Error getting wellness data for {user_id}: {e}")
            raise WellnessServiceException("Failed to get wellness data") 