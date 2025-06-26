from sanic import Blueprint, response, Request
from app.db.config import DB_NAME
from app.services.home_service import get_home_data

home_bp = Blueprint('home', url_prefix='/home')

@home_bp.route('/')
async def home_handler(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_home_data(request.app.ctx.mongo, DB_NAME, user_id)
    if data:
        return response.json(data)
    return response.json({"error": "Home data not found"}, status=404)
