from sanic import Blueprint, response, Request

home_bp = Blueprint('home', url_prefix='/home')

async def home_handler(request: Request):
    return response.json({
        "userName": "John Doe",
        "healthScore": 85,
        "dailyGoals": [
            {"id": 1, "title": "Steps", "current": 7500, "target": 10000, "unit": "steps", "progress": 75},
            {"id": 2, "title": "Water Intake", "current": 6, "target": 8, "unit": "glasses", "progress": 75},
            {"id": 3, "title": "Sleep", "current": 7, "target": 8, "unit": "hours", "progress": 87.5}
        ],
        "recentActivities": [
            {"id": 1, "type": "exercise", "title": "Morning Walk", "duration": "30 mins", "timestamp": "2025-06-26T06:30:00Z"},
            {"id": 2, "type": "meal", "title": "Healthy Breakfast", "calories": 350, "timestamp": "2025-06-26T08:00:00Z"}
        ],
        "upcomingAppointments": [
            {"id": 1, "type": "doctor", "title": "Annual Checkup", "date": "2025-06-28", "time": "10:00 AM", "doctor": "Dr. Smith"}
        ]
    })

home_bp.add_route(home_handler, '/')
