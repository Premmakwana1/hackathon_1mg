from sanic import Blueprint, response, Request
from app.services.search_service import get_search_suggestions, search_query_results
from app.services.fallback_service import FallbackService
from app.db.config import DB_NAME
from sanic.log import logger

search_bp = Blueprint('search', url_prefix='/search')

@search_bp.route('/')
async def search_suggestions(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    
    try:
        data = await get_search_suggestions(request.app.ctx.mongo)
        
        # Check if we should fallback to mock data
        if FallbackService.should_fallback(data):
            logger.warning(f"Search v2 API returned empty/error for user {user_id}, falling back to mock data")
            data = FallbackService.get_search_suggestions_fallback()
            data["_fallback"] = True
        
        return response.json(data)
        
    except Exception as e:
        logger.error(f"Error in search v2 API for user {user_id}: {str(e)}, falling back to mock data")
        data = FallbackService.get_search_suggestions_fallback()
        data["_fallback"] = True
        return response.json(data)

@search_bp.route('/query', methods=["POST"])
async def search_query(request: Request):
    body = request.json
    query = body.get('query', '')
    if not query:
        return response.json({"error": "Query is required"}, status=400)
    
    try:
        data = await search_query_results(request.app.ctx.mongo, query)
        
        # Check if we should fallback to mock data
        if FallbackService.should_fallback(data):
            logger.warning(f"Search query v2 API returned empty/error for query '{query}', falling back to mock data")
            data = FallbackService.get_search_results_fallback_with_query(query)
            data["_fallback"] = True
        
        return response.json(data)
        
    except Exception as e:
        logger.error(f"Error in search query v2 API for query '{query}': {str(e)}, falling back to mock data")
        data = FallbackService.get_search_results_fallback_with_query(query)
        data["_fallback"] = True
        return response.json(data) 