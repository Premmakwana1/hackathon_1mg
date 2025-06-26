"""
Service for activity tracking (steps, water, sleep, weight, meditation, etc.)
"""

import uuid
from app.models.launchpad.activity_tracker import ActivityTracker, Activity
from motor.motor_asyncio import AsyncIOMotorClient
from sanic import Sanic
from sanic.log import logger
from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
from pymongo import ASCENDING
from calendar import monthrange
from app.db.config import DB_NAME

class ActivityServiceException(Exception):
    pass

class ActivityService:
    def __init__(self, app: Sanic):
        self.app = app
        self.collection = app.ctx.mongo['launchpad_db']['activity_tracker']
        self.field_map = {
            "steps": "steps",
            "water": "glasses",
            "sleep": "duration",
            "weight": "value",
            "calories": "calories",
            "distance": "distance",
            "move_minutes": "activeMinutes",
            # Add more mappings as needed
        }

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['activity_tracker']
            try:
                await collection.create_index([('user_id', ASCENDING)])
                await collection.create_index([('activities.timestamp', ASCENDING)])
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def get_activity_summary(self, user_id: str) -> Optional[Dict]:
        """Return a summary of all tracked activities for the user."""
        try:
            doc = await self.collection.find_one({"user_id": user_id})
            if doc:
                return ActivityTracker(**doc).dict()
            return None
        except Exception as e:
            logger.error(f"Error fetching activity summary for {user_id}: {e}")
            raise ActivityServiceException("Failed to fetch activity summary")

    async def add_activity_entry(self, user_id: str, activity_type: str, value: dict) -> int:
        """Add a new entry for a specific activity type. Returns the new entry's id as int."""
        try:
            # Validate input using Activity model
            activity_id = int(datetime.utcnow().timestamp() * 1000)
            activity = Activity(
                id=activity_id,
                type=activity_type,
                title=value.get('title', activity_type.title()),
                duration=value.get('duration', 0),
                calories=value.get('calories', 0),
                steps=value.get('steps', 0),
                timestamp=value.get('timestamp', datetime.utcnow().isoformat()),
                intensity=value.get('intensity', 'normal')
            )
            await self.collection.update_one(
                {"user_id": user_id},
                {"$push": {"activities": activity.dict()}},
                upsert=True
            )
            return activity_id
        except Exception as e:
            logger.error(f"Error adding activity entry for {user_id}: {e}")
            raise ActivityServiceException("Failed to add activity entry")

    async def get_activity_history(self, user_id: str, activity_type: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Activity]:
        """Return the history of a specific activity for the user, optionally filtered by date range (ISO format)."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return []
            activities = [Activity(**a) for a in doc["activities"] if a["type"] == activity_type]
            if start_date or end_date:
                def in_range(a):
                    ts = datetime.fromisoformat(a.timestamp)
                    if start_date and ts < datetime.fromisoformat(start_date):
                        return False
                    if end_date and ts > datetime.fromisoformat(end_date):
                        return False
                    return True
                activities = [a for a in activities if in_range(a)]
            return activities
        except Exception as e:
            logger.error(f"Error fetching activity history for {user_id}: {e}")
            raise ActivityServiceException("Failed to fetch activity history")

    async def get_daily_totals(self, user_id: str, date: str) -> Dict[str, float]:
        """Return totals per activity type for a given date (ISO format)."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return {}
            totals = {}
            for a in doc["activities"]:
                ts = datetime.fromisoformat(a["timestamp"])
                if ts.date() == datetime.fromisoformat(date).date():
                    t = a["type"]
                    totals[t] = totals.get(t, 0) + a.get("steps", 0)
            return totals
        except Exception as e:
            logger.error(f"Error calculating daily totals for {user_id}: {e}")
            raise ActivityServiceException("Failed to calculate daily totals")

    async def get_weekly_averages(self, user_id: str, activity_type: str) -> float:
        """Return the 7-day average for a given activity type."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return 0.0
            now = datetime.utcnow()
            week_ago = now.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=6)
            values = [a.get("steps", 0) for a in doc["activities"] if a["type"] == activity_type and week_ago <= datetime.fromisoformat(a["timestamp"]) <= now]
            if not values:
                return 0.0
            return sum(values) / len(values)
        except Exception as e:
            logger.error(f"Error calculating weekly average for {user_id}: {e}")
            raise ActivityServiceException("Failed to calculate weekly average")

    async def delete_activity_entry(self, user_id: str, entry_id: str) -> bool:
        """Delete an activity entry by its id."""
        try:
            result = await self.collection.update_one(
                {"user_id": user_id},
                {"$pull": {"activities": {"id": entry_id}}}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error deleting activity entry for {user_id}: {e}")
            raise ActivityServiceException("Failed to delete activity entry")

    async def update_activity_entry(self, user_id: str, entry_id: str, updates: dict) -> bool:
        """Update an activity entry by its id."""
        try:
            # Validate updates using Activity model (partial)
            update_fields = {f"activities.$.{k}": v for k, v in updates.items()}
            result = await self.collection.update_one(
                {"user_id": user_id, "activities.id": entry_id},
                {"$set": update_fields}
            )
            return result.modified_count > 0
        except Exception as e:
            logger.error(f"Error updating activity entry for {user_id}: {e}")
            raise ActivityServiceException("Failed to update activity entry")

    async def get_monthly_history(self, user_id: str, activity_type: str, year: int, month: int) -> List[Dict[str, Any]]:
        """Return a list of daily values for a month for the given activity_type (for calendar view)."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return []
            days_in_month = monthrange(year, month)[1]
            daily = [0] * days_in_month
            metric = self.field_map.get(activity_type, None)
            for a in doc["activities"]:
                if a["type"] == activity_type:
                    ts = datetime.fromisoformat(a["timestamp"])
                    if ts.year == year and ts.month == month:
                        day = ts.day - 1
                        if metric and metric in a:
                            daily[day] += a.get(metric, 0)
            return [{"day": i+1, "value": daily[i]} for i in range(days_in_month)]
        except Exception as e:
            logger.error(f"Error getting monthly history for {user_id}: {e}")
            raise ActivityServiceException("Failed to get monthly history")

    async def get_lifetime_totals(self, user_id: str) -> Dict[str, float]:
        """Return total for each tracker type since account creation."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return {}
            totals = {}
            for a in doc["activities"]:
                t = a["type"]
                metric = self.field_map.get(t, None)
                if metric and metric in a:
                    totals[t] = totals.get(t, 0) + a.get(metric, 0)
            return totals
        except Exception as e:
            logger.error(f"Error getting lifetime totals for {user_id}: {e}")
            raise ActivityServiceException("Failed to get lifetime totals")

    async def get_last_sync_time(self, user_id: str, activity_type: str) -> Optional[str]:
        """Return the last sync timestamp for a tracker (activity_type), if available."""
        try:
            doc = await self.collection.find_one({"user_id": user_id}, {"activities": 1})
            if not doc or "activities" not in doc:
                return None
            # Find the latest timestamp for the given activity_type
            timestamps = [a["timestamp"] for a in doc["activities"] if a["type"] == activity_type]
            if not timestamps:
                return None
            return max(timestamps)
        except Exception as e:
            logger.error(f"Error getting last sync time for {user_id}: {e}")
            raise ActivityServiceException("Failed to get last sync time")

async def get_activity_dashboard(mongo, user_id):
    doc = await mongo[DB_NAME]['activities'].find_one({"user_id": user_id})
    if not doc:
        return None
    return doc.get("dashboard", {})

async def log_activity(mongo, user_id, activity_data):
    result = await mongo[DB_NAME]['activities'].update_one(
        {"user_id": user_id},
        {"$push": {"logs": activity_data}},
        upsert=True
    )
    return {"success": True, "activityId": str(activity_data.get("id", ""))}

async def update_activity_goals(mongo, user_id, goals_data):
    result = await mongo[DB_NAME]['activities'].update_one(
        {"user_id": user_id},
        {"$set": {"goals": goals_data}},
        upsert=True
    )
    return {"success": True, "updatedGoals": goals_data} 