from sanic import Blueprint, response, Request

search_bp = Blueprint('search', url_prefix='/search')

@search_bp.route('/')
async def search_get(request: Request):
    return response.json({
        "suggestions": ["Weight loss exercises", "Healthy breakfast recipes", "Stress management techniques"],
        "popularSearches": ["cardio workout", "meditation", "protein recipes"],
        "filters": {"categories": ["All", "Exercise", "Nutrition"], "difficulty": ["All", "Beginner"], "duration": ["All", "10-30 min"]}
    })

@search_bp.route('/query', methods=["POST"])
async def search_query(request: Request):
    return response.json({
        "results": [
            {"id": 1, "type": "exercise", "title": "Push-ups", "description": "Chest and arm strengthening exercise"},
            {"id": 2, "type": "recipe", "title": "Protein Smoothie", "description": "High-protein breakfast smoothie"}
        ],
        "totalCount": 2,
        "suggestions": ["Try yoga", "Healthy snacks"]
    }) 