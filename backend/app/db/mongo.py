import motor.motor_asyncio
from sanic.log import logger
from app.db.config import MONGO_URI

async def init_mongo(app):
    app.ctx.mongo = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    logger.info(f"MongoDB connected: {MONGO_URI}") 