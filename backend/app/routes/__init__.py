from sanic import Blueprint
from .wellness_config import wellness_config_bp
from .home import home_bp
from .wellness import wellness_bp
from .onboarding import onboarding_bp
from .profile import profile_bp
from .goals import goals_bp
from .trackers import trackers_bp
from .hra import hra_bp

v1_blueprints = Blueprint.group(
    wellness_config_bp,
    home_bp,
    wellness_bp,
    onboarding_bp,
    profile_bp,
    goals_bp,
    trackers_bp,
    hra_bp,
    url_prefix="/api",
    version=1,
) 