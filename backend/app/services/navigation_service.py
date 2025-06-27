from app.db.config import DB_NAME

async def save_continue(mongo, user_id, data):
    await mongo[DB_NAME]['user'].update_one(
        {"id": int(user_id)},
        {"$set": {"navigation": {"continue": data}}},
        upsert=True
    )
    return {"success": True, "nextRoute": data.get("nextRoute"), "nextStep": data.get("nextStep"), "message": data.get("message")}

async def save_exit(mongo, user_id, data):
    await mongo[DB_NAME]['user'].update_one(
        {"id": int(user_id)},
        {"$set": {"navigation": {"exit": data}}},
        upsert=True
    )
    return {"success": True, "resumeToken": data.get("resumeToken"), "message": data.get("message")} 