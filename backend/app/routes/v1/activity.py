from sanic import Blueprint, response, Request

activity_bp = Blueprint('activity', url_prefix='/activity')

@activity_bp.route('/dashboard')
async def activity_dashboard(request: Request):
    return response.json({
        "todayStats": {"steps": 8000, "calories": 500, "activeMinutes": 45},
        "weeklyStats": {"steps": 56000, "calories": 3500, "activeMinutes": 315},
        "activities": [
            {"id": 1, "type": "walk", "title": "Morning Walk", "duration": 30, "calories": 120, "timestamp": "2025-06-26T06:30:00Z"},
            {"id": 2, "type": "yoga", "title": "Yoga Session", "duration": 45, "calories": 180, "timestamp": "2025-06-25T07:00:00Z"}
        ],
        "goals": {"steps": 10000, "calories": 600, "activeMinutes": 60},
        "achievements": [
            {"id": 1, "title": "10K Steps!", "description": "You walked 10,000 steps in a day!", "date": "2025-06-24"}
        ]
    })

@activity_bp.route('/log', methods=["POST"])
async def activity_log(request: Request):
    return response.json({
        "success": True,
        "activityId": "activity_123",
        "updatedStats": {"steps": 8500, "calories": 520, "activeMinutes": 50}
    })

@activity_bp.route('/goals/update', methods=["POST"])
async def activity_goals_update(request: Request):
    return response.json({
        "success": True,
        "updatedGoals": {"steps": 12000, "calories": 700, "activeMinutes": 70}
    }) 