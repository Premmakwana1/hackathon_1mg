from sanic import Blueprint, response, Request
from app.services.hra_service import get_hra_step, save_hra_step, get_hra_report
from app.db.config import DB_NAME

hra_bp = Blueprint('hra', url_prefix='/hra')

@hra_bp.route('/<step:int>')
async def hra_step(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_hra_step(request.app.ctx.mongo, user_id, step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)

@hra_bp.route('/<step:int>/save', methods=["POST"])
async def hra_save(request: Request, step: int):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    step_data = request.json
    result = await save_hra_step(request.app.ctx.mongo, user_id, step, step_data)
    return response.json(result)

@hra_bp.route('/report')
async def hra_report(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_hra_report(request.app.ctx.mongo, user_id)
    if not data:
        return response.json({"error": "No report found"}, status=404)
    return response.json(data) 