from sanic import Blueprint, response, Request
from app.services.wellness_service import get_wellness_intro
from app.utils.fallback_decorator import with_fallback
from app.db.config import DB_NAME

wellness_bp = Blueprint('wellness', url_prefix='/wellness')

@wellness_bp.route('/intro')
@with_fallback('wellness_intro')
async def wellness_intro(request: Request):
    user_id = request.args.get('user_id') or request.headers.get('user-id')
    if not user_id:
        return response.json({"error": "Missing user_id"}, status=400)
    data = await get_wellness_intro(request.app.ctx.mongo, user_id)
    return response.json(data)
