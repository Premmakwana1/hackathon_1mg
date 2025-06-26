from sanic import Blueprint, response, Request

user_progress_bp = Blueprint('user_progress', url_prefix='/user/progress')

@user_progress_bp.route('/')
async def user_progress_get(request: Request):
    return response.json({
        "completionStatus": {"onboarding": True, "profile": False, "hra": False},
        "currentStep": {"onboarding": 5, "profile": 2, "hra": 1},
        "overallProgress": 60
    })

@user_progress_bp.route('/update', methods=["POST"])
async def user_progress_update(request: Request):
    return response.json({
        "success": True,
        "updatedProgress": {"onboarding": True, "profile": True, "hra": True}
    }) 