from app.db.config import DB_NAME

ONBOARDING_MOCK = {
    1: {
        "step": 1,
        "totalSteps": 5,
        "title": "Welcome to Your Health Journey",
        "description": "Let's get started by understanding your health goals and preferences.",
        "options": [],
        "isCompleted": False
    },
    2: {
        "step": 2,
        "totalSteps": 5,
        "title": "What's Your Primary Health Goal?",
        "description": "Choose the goal that matters most to you right now.",
        "options": [
            {"id": 1, "title": "Weight Management", "icon": "scale"},
            {"id": 2, "title": "Fitness Improvement", "icon": "fitness"},
            {"id": 3, "title": "Better Sleep", "icon": "sleep"},
            {"id": 4, "title": "Stress Management", "icon": "meditation"}
        ],
        "isCompleted": False
    },
    3: {
        "step": 3,
        "totalSteps": 5,
        "title": "How Active Are You?",
        "description": "Help us understand your current activity level.",
        "options": [
            {"id": 1, "title": "Sedentary", "description": "Little to no exercise"},
            {"id": 2, "title": "Lightly Active", "description": "Light exercise 1-3 days/week"},
            {"id": 3, "title": "Moderately Active", "description": "Moderate exercise 3-5 days/week"},
            {"id": 4, "title": "Very Active", "description": "Hard exercise 6-7 days/week"}
        ],
        "isCompleted": False
    },
    4: {
        "step": 4,
        "totalSteps": 5,
        "title": "Enable Notifications",
        "description": "Stay on track with gentle reminders and health tips.",
        "options": [
            {"id": 1, "title": "Daily Reminders", "enabled": True},
            {"id": 2, "title": "Weekly Reports", "enabled": True},
            {"id": 3, "title": "Health Tips", "enabled": False}
        ],
        "isCompleted": False
    },
    5: {
        "step": 5,
        "totalSteps": 5,
        "title": "You're All Set!",
        "description": "Your personalized health journey starts now.",
        "options": [],
        "isCompleted": True
    }
}

async def get_onboarding_step(mongo, user_id, step):
    doc = await mongo[DB_NAME]['onboarding'].find_one({"user_id": user_id})
    if not doc or "steps" not in doc:
        return None
    for s in doc["steps"]:
        if s.get("step") == step:
            return s
    return None

async def save_onboarding_step(mongo, user_id, step, step_data):
    doc = await mongo[DB_NAME]['onboarding'].find_one({"user_id": user_id})
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
    await mongo[DB_NAME]['onboarding'].update_one(
        {"user_id": user_id},
        {"$set": {"steps": steps}},
        upsert=True
    )
    return {"success": True, "nextStep": step + 1} 