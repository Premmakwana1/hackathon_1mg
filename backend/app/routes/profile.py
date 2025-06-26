from sanic import Blueprint, response, Request

profile_bp = Blueprint('profile', url_prefix='/profile')

PROFILE_MOCK = {
    1: {
        "step": 1,
        "questions": [
            {"id": "age", "type": "number", "label": "What's your age?", "placeholder": "Enter your age", "required": True, "validation": {"min": 13, "max": 120}},
            {"id": "gender", "type": "radio", "label": "Select your gender", "required": True, "options": [
                {"value": "male", "label": "Male", "icon": "male"},
                {"value": "female", "label": "Female", "icon": "female"},
                {"value": "other", "label": "Others", "icon": "other"}
            ]}
        ],
        "userResponses": {},
        "validationErrors": {}
    },
    2: {
        "step": 2,
        "questions": [
            {"id": "height", "type": "number", "label": "What's your height?", "placeholder": "Enter height in cm", "required": True, "validation": {"min": 50, "max": 250}},
            {"id": "weight", "type": "number", "label": "What's your current weight?", "placeholder": "Enter weight in kg", "required": True, "validation": {"min": 20, "max": 300}}
        ],
        "userResponses": {},
        "validationErrors": {}
    },
    3: {
        "step": 3,
        "questions": [
            {"id": "medicalConditions", "type": "checkbox", "label": "Do you have any of these medical conditions?", "required": False, "options": [
                {"value": "diabetes", "label": "Diabetes"},
                {"value": "hypertension", "label": "High Blood Pressure"},
                {"value": "heart_disease", "label": "Heart Disease"},
                {"value": "asthma", "label": "Asthma"},
                {"value": "none", "label": "None of the above"}
            ]},
            {"id": "medications", "type": "textarea", "label": "Are you currently taking any medications?", "placeholder": "List your current medications (optional)", "required": False}
        ],
        "userResponses": {},
        "validationErrors": {}
    }
}

@profile_bp.route('/basic/<step:int>')
async def basic_profile_step(request: Request, step: int):
    data = PROFILE_MOCK.get(step)
    if not data:
        return response.json({"error": "Step not found"}, status=404)
    return response.json(data)
