from sanic import Blueprint, response, Request
from app.services.activity_service import get_activity_dashboard, log_activity, update_activity_goals
from app.utils.fallback_decorator import with_fallback
from app.db.config import DB_NAME

activity_bp = Blueprint('activity', url_prefix='/activity')

@activity_bp.route('/dashboard')
@with_fallback('activity_dashboard')
async def activity_dashboard(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_activity_dashboard(request.app.ctx.mongo, user_id)
    if not data:
        return response.json({"error": "No dashboard data found"}, status=404)
    return response.json(data)

@activity_bp.route('/log', methods=["POST"])
@with_fallback('activity_log')
async def activity_log(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    activity_data = request.json
    result = await log_activity(request.app.ctx.mongo, user_id, activity_data)
    return response.json(result)

@activity_bp.route('/goals/update', methods=["POST"])
@with_fallback('activity_goals')
async def activity_goals_update(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    goals_data = request.json
    result = await update_activity_goals(request.app.ctx.mongo, user_id, goals_data)
    return response.json(result) 