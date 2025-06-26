from app.db.config import DB_NAME

async def get_search_suggestions(mongo):
    doc = await mongo[DB_NAME]['search'].find_one({"type": "suggestions"})
    return doc.get("data", {}) if doc else {}

async def search_query_results(mongo, query):
    # For demo, just return all results that match the query in 'title' or 'description'
    cursor = mongo[DB_NAME]['search'].find({
        "$or": [
            {"title": {"$regex": query, "$options": "i"}},
            {"description": {"$regex": query, "$options": "i"}}
        ]
    })
    results = []
    async for doc in cursor:
        results.append(doc)
    return {"results": results, "totalCount": len(results)}

def get_search_suggestions():
    return {
        "suggestions": ["Weight loss exercises", "Healthy breakfast recipes", "Stress management techniques"],
        "popularSearches": ["cardio workout", "meditation", "protein recipes"],
        "filters": {"categories": ["All", "Exercise", "Nutrition"], "difficulty": ["All", "Beginner"], "duration": ["All", "10-30 min"]}
    }

def search_query_results():
    return {
        "results": [
            {"id": 1, "type": "exercise", "title": "Push-ups", "description": "Chest and arm strengthening exercise"},
            {"id": 2, "type": "recipe", "title": "Protein Smoothie", "description": "High-protein breakfast smoothie"}
        ],
        "totalCount": 2,
        "suggestions": ["Try yoga", "Healthy snacks"]
    } 