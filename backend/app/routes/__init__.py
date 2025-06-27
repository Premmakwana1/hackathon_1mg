from sanic import Blueprint
from .v1.home import home_bp as home_v1_bp
from .v1.wellness_config import wellness_config_bp as wellness_config_v1_bp
from .v1.wellness import wellness_bp as wellness_v1_bp
from .v1.onboarding import onboarding_bp as onboarding_v1_bp
from .v1.profile import profile_bp as profile_v1_bp
from .v1.goals import goals_bp as goals_v1_bp
from .v1.trackers import trackers_bp as trackers_v1_bp
from .v1.hra import hra_bp as hra_v1_bp
from .v1.activity import activity_bp as activity_v1_bp
from .v1.search import search_bp as search_v1_bp
from .v1.user_progress import user_progress_bp as user_progress_v1_bp
from .v1.navigation import navigation_bp as navigation_v1_bp

from .v2.home import home_bp as home_v2_bp
from .v2.wellness_config import wellness_config_bp as wellness_config_v2_bp
from .v2.wellness import wellness_bp as wellness_v2_bp
from .v2.onboarding import onboarding_bp as onboarding_v2_bp
from .v2.profile import profile_bp as profile_v2_bp
from .v2.goals import goals_bp as goals_v2_bp
from .v2.trackers import trackers_bp as trackers_v2_bp
from .v2.hra import hra_bp as hra_v2_bp
from .v2.activity import activity_bp as activity_v2_bp
from .v2.search import search_bp as search_v2_bp
from .v2.user_progress import user_progress_bp as user_progress_v2_bp
from .v2.navigation import navigation_bp as navigation_v2_bp

v1_blueprints = Blueprint.group(
    wellness_config_v1_bp,
    home_v1_bp,
    wellness_v1_bp,
    onboarding_v1_bp,
    profile_v1_bp,
    goals_v1_bp,
    trackers_v1_bp,
    hra_v1_bp,
    activity_v1_bp,
    search_v1_bp,
    user_progress_v1_bp,
    navigation_v1_bp,
    url_prefix="/v1/api"
)

v2_blueprints = Blueprint.group(
    wellness_config_v2_bp,
    home_v2_bp,
    wellness_v2_bp,
    onboarding_v2_bp,
    profile_v2_bp,
    goals_v2_bp,
    trackers_v2_bp,
    hra_v2_bp,
    activity_v2_bp,
    search_v2_bp,
    user_progress_v2_bp,
    navigation_v2_bp,
    url_prefix="/v1/api"
)

def get_api_blueprints(version: str):
    if version == "v2":
        return v2_blueprints
    return v1_blueprints 