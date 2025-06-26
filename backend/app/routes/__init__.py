from sanic import Blueprint
from .wellness_config import wellness_config_bp
from .home import home_bp
from .wellness import wellness_bp
from .onboarding import onboarding_bp
from .profile import profile_bp
from .goals import goals_bp
from .trackers import trackers_bp
from .hra import hra_bp
from .activity import activity_bp
from .search import search_bp
from .user_progress import user_progress_bp
from .navigation import navigation_bp

v1_blueprints = Blueprint.group(
    wellness_config_bp,
    home_bp,
    wellness_bp,
    onboarding_bp,
    profile_bp,
    goals_bp,
    trackers_bp,
    hra_bp,
    activity_bp,
    search_bp,
    user_progress_bp,
    navigation_bp,
    url_prefix="/v1/api"
) 