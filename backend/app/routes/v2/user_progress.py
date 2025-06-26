from sanic import Blueprint, response, Request
from app.services.user_progress_service import get_user_progress, update_user_progress
from app.db.config import DB_NAME

user_progress_bp = Blueprint('user_progress', url_prefix='/user/progress')

@user_progress_bp.route('/')
async def user_progress_get(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_user_progress(request.app.ctx.mongo, user_id)
    return response.json(data)

@user_progress_bp.route('/update', methods=["POST"])
async def user_progress_update(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    progress_data = await request.json()
    result = await update_user_progress(request.app.ctx.mongo, user_id, progress_data)
    return response.json(result) 