from sanic import Blueprint, response, Request
from app.db.config import DB_NAME
from app.services.home_service import get_home_data
from app.services.fallback_service import FallbackService
from sanic.log import logger

home_bp = Blueprint('home', url_prefix='/home')

@home_bp.route('/')
async def home_handler(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    
    try:
        # Try to get data from v2 service
        data = await get_home_data(request.app.ctx.mongo, DB_NAME, user_id)
        
        # Check if we should fallback to mock data
        if FallbackService.should_fallback(data):
            logger.warning(f"Home v2 API returned empty/error for user {user_id}, falling back to mock data")
            data = FallbackService.get_home_fallback(user_id)
            # Add fallback indicator
            data["_fallback"] = True
        
        return response.json(data)
        
    except Exception as e:
        logger.error(f"Error in home v2 API for user {user_id}: {str(e)}, falling back to mock data")
        data = FallbackService.get_home_fallback(user_id)
        data["_fallback"] = True
        return response.json(data)
