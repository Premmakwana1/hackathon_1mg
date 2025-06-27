from sanic import Blueprint, response, Request
from app.services.profile_service import ProfileService
from app.services.fallback_service import FallbackService
from app.db.config import DB_NAME
from sanic.log import logger

profile_bp = Blueprint('profile', url_prefix='/profile')

@profile_bp.route('/basic/<step:int>')
async def basic_profile_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    
    try:
        service = ProfileService(request.app)
        data = await service.get_profile_step(user_id, step)
        
        # Check if we should fallback to mock data
        if FallbackService.should_fallback(data):
            logger.warning(f"Profile v2 API returned empty/error for user {user_id} step {step}, falling back to mock data")
            data = FallbackService.get_profile_fallback(step)
            if data:
                data["_fallback"] = True
            else:
                return response.json({"error": "Step not found"}, status=404)
        
        return response.json(data)
        
    except Exception as e:
        logger.error(f"Error in profile v2 API for user {user_id} step {step}: {str(e)}, falling back to mock data")
        data = FallbackService.get_profile_fallback(step)
        if data:
            data["_fallback"] = True
            return response.json(data)
        else:
            return response.json({"error": "Step not found"}, status=404)

@profile_bp.route('/basic/<step:int>/save', methods=["POST"])
async def profile_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    
    print('DEBUG request.json:', request.json)
    step_data = request.json
    
    try:
        service = ProfileService(request.app)
        result = await service.save_profile_step(user_id, step, step_data)
        
        # Check if we should fallback to mock data
        if FallbackService.should_fallback(result):
            logger.warning(f"Profile save v2 API returned empty/error for user {user_id} step {step}, falling back to mock data")
            result = {
                "success": True,
                "validationErrors": {},
                "nextStep": step + 1,
                "_fallback": True
            }
        
        return response.json(result)
        
    except Exception as e:
        logger.error(f"Error in profile save v2 API for user {user_id} step {step}: {str(e)}, falling back to mock data")
        result = {
            "success": True,
            "validationErrors": {},
            "nextStep": step + 1,
            "_fallback": True
        }
        return response.json(result)
