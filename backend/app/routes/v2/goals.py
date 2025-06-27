from sanic import Blueprint, response, Request
from app.services.goals_service import get_goals_step, save_goals_step
from app.db.config import DB_NAME

goals_bp = Blueprint('goals', url_prefix='/goals')

@goals_bp.route('/<step:int>')
async def goals_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_goals_step(request.app.ctx.mongo, user_id, step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@goals_bp.route('/<step:int>/save', methods=["POST"])
async def goals_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    step_data = request.json
    result = await save_goals_step(request.app.ctx.mongo, user_id, step, step_data)
    return response.json(result)
