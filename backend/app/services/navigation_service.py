def save_continue():
    return {
        "success": True,
        "nextRoute": "/api/v1/onboarding/2",
        "nextStep": 2,
        "message": "Progress saved. Continue to next step."
    }

def save_exit():
    return {
        "success": True,
        "resumeToken": "resume_abc123",
        "message": "Progress saved. You can resume later."
    } 