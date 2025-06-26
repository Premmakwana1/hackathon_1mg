from sanic import Blueprint, response, Request
from app.services.launchpad.user_service import get_user_config

wellness_config_bp = Blueprint('wellness_config', url_prefix='/api/wellness')

def to_camel_case(s):
    parts = s.split('_')
    return parts[0] + ''.join(word.capitalize() for word in parts[1:])

def keys_to_camel(obj):
    if isinstance(obj, list):
        return [keys_to_camel(i) for i in obj]
    elif isinstance(obj, dict):
        return {to_camel_case(k): keys_to_camel(v) for k, v in obj.items()}
    else:
        return obj

@wellness_config_bp.route('/config')
async def wellness_config(request: Request):
    user_config = await get_user_config(request.app)
    camel_config = keys_to_camel(user_config.model_dump())
    return response.json(camel_config) 