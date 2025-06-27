from app.db.config import DB_NAME

async def get_search_suggestions(mongo):
    doc = await mongo[DB_NAME]['search'].find_one({"type": "suggestions"})
    if doc and doc.get("data"):
        return doc.get("data")
    return None  # Return None to trigger fallback

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
    
    if results:
        return {"results": results, "totalCount": len(results)}
    return None  # Return None to trigger fallback 