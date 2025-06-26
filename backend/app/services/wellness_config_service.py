from app.services.launchpad.user_service import get_user_config

async def get_wellness_config(app):
    user_config = await get_user_config(app)
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
    return keys_to_camel(user_config.model_dump()) 