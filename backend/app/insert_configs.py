import os
import json
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import sys

# Import config logic from backend/app/db/config.py
from db.config import MONGO_URI, DB_NAME

# Path to the newMockData directory (relative to project root)
NEWMOCKDATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../api/newMockData'))

async def insert_configs():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db['configs']

    for filename in os.listdir(NEWMOCKDATA_DIR):
        if filename.endswith('.json'):
            key = filename.replace('.json', '')
            with open(os.path.join(NEWMOCKDATA_DIR, filename), 'r') as f:
                value = json.load(f)
            # Upsert: update if exists, insert if not
            result = await collection.update_one(
                {"key": key},
                {"$set": {"value": value}},
                upsert=True
            )
            print(f"Inserted/Updated config for key: {key}")
    print("All configs inserted/updated.")
    client.close()

if __name__ == "__main__":
    asyncio.run(insert_configs()) 