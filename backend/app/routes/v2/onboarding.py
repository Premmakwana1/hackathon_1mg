from sanic import Blueprint, response, Request
from app.services.onboarding_service import get_onboarding_step, save_onboarding_step
from app.utils.fallback_decorator import with_step_fallback
from app.db.config import DB_NAME

onboarding_bp = Blueprint('onboarding', url_prefix='/onboarding')

@onboarding_bp.route('/<step:int>')
@with_step_fallback('onboarding')
async def onboarding_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_onboarding_step(request.app.ctx.mongo, user_id, step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@onboarding_bp.route('/<step:int>/save', methods=["POST"])
@with_step_fallback('onboarding')
async def onboarding_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    step_data = request.json
    result = await save_onboarding_step(request.app.ctx.mongo, user_id, step, step_data)
    return response.json(result)
