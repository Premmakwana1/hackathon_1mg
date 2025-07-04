from sanic import Blueprint, response, Request

onboarding_bp = Blueprint('onboarding', url_prefix='/onboarding')

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

@onboarding_bp.route('/<step:int>')
async def onboarding_step(request: Request, step: int):
    data = ONBOARDING_MOCK.get(step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@onboarding_bp.route('/<step:int>/save', methods=["POST"])
async def onboarding_save(request: Request, step: int):
    # Mock response for saving onboarding step
    return response.json({
        "success": True,
        "nextStep": step + 2,
        "message": f"Step {step} saved successfully."
    })
