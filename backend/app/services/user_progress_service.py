from app.db.config import DB_NAME

async def get_user_progress(mongo, user_id):
    doc = await mongo[DB_NAME]['user'].find_one({"id": int(user_id)})
    return doc.get("progress", {}) if doc else {}

async def update_user_progress(mongo, user_id, progress_data):
    await mongo[DB_NAME]['user'].update_one(
        {"id": int(user_id)},
        {"$set": {"progress": progress_data}},
        upsert=True
    )
    return {"success": True, "updatedProgress": progress_data} 