from sanic import Blueprint, response, Request
from app.services.profile_service import ProfileService
from app.db.config import DB_NAME

profile_bp = Blueprint('profile', url_prefix='/profile')

@profile_bp.route('/basic/<step:int>')
async def basic_profile_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    service = ProfileService(request.app)
    data = await service.get_profile_step(user_id, step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@profile_bp.route('/basic/<step:int>/save', methods=["POST"])
async def profile_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    print('DEBUG request.json:', request.json)
    step_data = request.json
    service = ProfileService(request.app)
    result = await service.save_profile_step(user_id, step, step_data)
    return response.json(result)
