from sanic import Blueprint, response, Request

navigation_bp = Blueprint('navigation', url_prefix='/navigation')

@navigation_bp.route('/save-continue', methods=["POST"])
async def navigation_save_continue(request: Request):
    return response.json({
        "success": True,
        "nextRoute": "/api/v1/onboarding/2",
        "nextStep": 2,
        "message": "Progress saved. Continue to next step."
    })

@navigation_bp.route('/save-exit', methods=["POST"])
async def navigation_save_exit(request: Request):
    return response.json({
        "success": True,
        "resumeToken": "resume_abc123",
        "message": "Progress saved. You can resume later."
    }) 