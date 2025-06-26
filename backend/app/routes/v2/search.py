from sanic import Blueprint, response, Request
from app.services.search_service import get_search_suggestions, search_query_results
from app.db.config import DB_NAME

search_bp = Blueprint('search', url_prefix='/search')

@search_bp.route('/')
async def search_get(request: Request):
    data = await get_search_suggestions(request.app.ctx.mongo)
    return response.json(data)

@search_bp.route('/query', methods=["POST"])
async def search_query(request: Request):
    body = await request.json()
    query = body.get('query', '')
    data = await search_query_results(request.app.ctx.mongo, query)
    return response.json(data) 