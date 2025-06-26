from sanic import Blueprint
from app.routes.v1.launchpad.wellness_config import wellness_config_bp

v1_blueprints = Blueprint.group(
    wellness_config_bp,
    version=1,
) 