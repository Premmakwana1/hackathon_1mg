from sanic import Blueprint, response, Request
from app.services.trackers_service import get_trackers_step, save_trackers_step
from app.utils.fallback_decorator import with_step_fallback
from app.db.config import DB_NAME

trackers_bp = Blueprint('trackers', url_prefix='/trackers')

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

@trackers_bp.route('/<step:int>')
@with_step_fallback('trackers')
async def trackers_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_trackers_step(request.app.ctx.mongo, user_id, step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@trackers_bp.route('/<step:int>/save', methods=["POST"])
@with_step_fallback('trackers')
async def trackers_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    step_data = request.json
    result = await save_trackers_step(request.app.ctx.mongo, user_id, step, step_data)
    return response.json(result) 