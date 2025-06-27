from sanic import Blueprint, response, Request
from app.services.navigation_service import save_continue, save_exit
from app.db.config import DB_NAME

navigation_bp = Blueprint('navigation', url_prefix='/navigation')

@navigation_bp.route('/save-continue', methods=["POST"])
async def navigation_save_continue(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = request.json
    result = await save_continue(request.app.ctx.mongo, user_id, data)
    return response.json(result)

@navigation_bp.route('/save-exit', methods=["POST"])
async def navigation_save_exit(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = request.json
    result = await save_exit(request.app.ctx.mongo, user_id, data)
    return response.json(result) 