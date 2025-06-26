"""
Service for user management (registration, authentication, etc.)
"""

import uuid
from datetime import datetime
from app.models.launchpad.user import User
from sanic import Sanic
from sanic.log import logger
from typing import Optional, Dict, Any
from pymongo import ASCENDING
from pydantic import BaseModel, EmailStr, ValidationError
import bcrypt

class UserPayload(BaseModel):
    email: EmailStr
    name: str
    password: str
    # Add other fields as needed

class UserServiceException(Exception):
    pass

class UserService:
    def __init__(self, app: Sanic, collection=None):
        self.app = app
        if collection is not None:
            self.collection = collection
        else:
            self.collection = app.ctx.mongo['launchpad_db']['users']

    @classmethod
    def register_listeners(cls, app: Sanic):
        @app.listener('before_server_start')
        async def ensure_indexes(app, loop):
            collection = app.ctx.mongo['launchpad_db']['users']
            try:
                await collection.create_index([('_id', ASCENDING)], unique=True)
                await collection.create_index([('email', ASCENDING)], unique=True)
            except Exception as e:
                logger.error(f"Failed to create indexes: {e}")

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Return user details as a sanitized dict."""
        try:
            doc = await self.collection.find_one({"_id": user_id})
            if doc:
                doc.pop('password_hash', None)
                return doc
            return None
        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            raise UserServiceException("Failed to get user")

    async def create_user(self, user_data: Dict[str, Any]) -> str:
        """Create a new user. Returns the user id. Hashes password and enforces unique email."""
        try:
            payload = UserPayload(**user_data)
            password_hash = bcrypt.hashpw(payload.password.encode(), bcrypt.gensalt()).decode()
            user_doc = {
                "_id": str(uuid.uuid4()),
                "email": payload.email,
                "name": payload.name,
                "password_hash": password_hash,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }
            await self.collection.insert_one(user_doc)
            return user_doc["_id"]
        except ValidationError as ve:
            logger.error(f"Validation error creating user: {ve}")
            raise UserServiceException("Invalid user data")
        except Exception as e:
            if hasattr(e, 'details') and 'duplicate key error' in str(e):
                logger.error(f"Duplicate email error: {e}")
                raise UserServiceException("Email already registered")
            logger.error(f"Error creating user: {e}")
            raise UserServiceException("Failed to create user")

    async def authenticate(self, email: str, password: str) -> Optional[str]:
        """Authenticate user by email and password. Returns user_id if valid, else None."""
        try:
            doc = await self.collection.find_one({"email": email})
            if doc and bcrypt.checkpw(password.encode(), doc["password_hash"].encode()):
                return doc["_id"]
            return None
        except Exception as e:
            logger.error(f"Error authenticating user {email}: {e}")
            raise UserServiceException("Failed to authenticate user") 