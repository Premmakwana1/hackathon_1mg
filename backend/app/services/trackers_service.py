from app.db.config import DB_NAME

TRACKERS_MOCK = {
    1: {
        "step": 1,
        "categories": [
            {"id": "fitness", "title": "Fitness Trackers", "description": "Monitor your physical activities"},
            {"id": "health", "title": "Health Monitors", "description": "Track vital health metrics"},
            {"id": "lifestyle", "title": "Lifestyle Trackers", "description": "Monitor daily habits and routines"}
        ],
        "availableTrackers": [
            {"id": "steps", "title": "Step Counter", "description": "Track daily steps and distance", "category": "fitness", "icon": "steps", "enabled": True, "defaultGoal": 10000},
            {"id": "calories", "title": "Calorie Tracker", "description": "Monitor calories burned and consumed", "category": "fitness", "icon": "calories", "enabled": False, "defaultGoal": 2000},
            {"id": "heart_rate", "title": "Heart Rate Monitor", "description": "Track resting and active heart rate", "category": "health", "icon": "heart", "enabled": False, "defaultGoal": 70},
            {"id": "sleep", "title": "Sleep Tracker", "description": "Monitor sleep duration and quality", "category": "lifestyle", "icon": "sleep", "enabled": True, "defaultGoal": 8}
        ],
        "selectedTrackers": ["steps", "sleep"]
    },
    2: {
        "step": 2,
        "categories": [
            {"id": "nutrition", "title": "Nutrition Trackers", "description": "Monitor your eating habits"},
            {"id": "mental_health", "title": "Mental Health", "description": "Track mood and stress levels"}
        ],
        "availableTrackers": [
            {"id": "water_intake", "title": "Water Intake", "description": "Track daily water consumption", "category": "nutrition", "icon": "water", "enabled": True, "defaultGoal": 8},
            {"id": "meal_log", "title": "Meal Logger", "description": "Log your meals and snacks", "category": "nutrition", "icon": "food", "enabled": False, "defaultGoal": 3},
            {"id": "mood", "title": "Mood Tracker", "description": "Monitor daily mood and emotions", "category": "mental_health", "icon": "mood", "enabled": False, "defaultGoal": 1},
            {"id": "meditation", "title": "Meditation Timer", "description": "Track meditation and mindfulness", "category": "mental_health", "icon": "meditation", "enabled": False, "defaultGoal": 10}
        ],
        "selectedTrackers": ["water_intake"]
    }
}

async def get_trackers_step(mongo, user_id, step):
    doc = await mongo[DB_NAME]['trackers'].find_one({"user_id": user_id})
    if not doc or "steps" not in doc:
        return None
    for s in doc["steps"]:
        if s.get("step") == step:
            return s
    return None

async def save_trackers_step(mongo, user_id, step, step_data):
    doc = await mongo[DB_NAME]['trackers'].find_one({"user_id": user_id})
    if not doc or "steps" not in doc:
        steps = [step_data]
    else:
        steps = doc["steps"]
        updated = False
        for idx, s in enumerate(steps):
            if s.get("step") == step:
                steps[idx] = step_data
                updated = True
                break
        if not updated:
            steps.append(step_data)
    await mongo[DB_NAME]['trackers'].update_one(
        {"user_id": user_id},
        {"$set": {"steps": steps}},
        upsert=True
    )
    return {"success": True, "nextStep": step + 1} 