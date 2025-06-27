from app.db.config import DB_NAME

HRA_MOCK = {
    1: {
        "step": 1,
        "questions": [
            {"id": "smoking", "type": "radio", "label": "Do you smoke?", "required": True, "options": [
                {"value": "never", "label": "Never smoked"},
                {"value": "former", "label": "Former smoker"},
                {"value": "current", "label": "Current smoker"}
            ]},
            {"id": "alcohol", "type": "radio", "label": "How often do you consume alcohol?", "required": True, "options": [
                {"value": "never", "label": "Never"},
                {"value": "occasionally", "label": "Occasionally (1-2 times/week)"},
                {"value": "regularly", "label": "Regularly (3+ times/week)"},
                {"value": "daily", "label": "Daily"}
            ]}
        ],
        "responses": {},
        "riskFactors": [],
        "recommendations": []
    },
    2: {
        "step": 2,
        "questions": [
            {"id": "exercise_frequency", "type": "radio", "label": "How often do you exercise?", "required": True, "options": [
                {"value": "never", "label": "Never"},
                {"value": "1-2_times", "label": "1-2 times per week"},
                {"value": "3-4_times", "label": "3-4 times per week"},
                {"value": "5+_times", "label": "5+ times per week"}
            ]},
            {"id": "diet_quality", "type": "radio", "label": "How would you rate your diet?", "required": True, "options": [
                {"value": "poor", "label": "Poor (mostly processed foods)"},
                {"value": "fair", "label": "Fair (some healthy choices)"},
                {"value": "good", "label": "Good (mostly healthy)"},
                {"value": "excellent", "label": "Excellent (very healthy)"}
            ]}
        ],
        "responses": {},
        "riskFactors": [],
        "recommendations": []
    },
    3: {
        "step": 3,
        "questions": [
            {"id": "family_history", "type": "checkbox", "label": "Do you have a family history of any of these conditions?", "required": False, "options": [
                {"value": "heart_disease", "label": "Heart Disease"},
                {"value": "diabetes", "label": "Diabetes"},
                {"value": "cancer", "label": "Cancer"},
                {"value": "stroke", "label": "Stroke"},
                {"value": "none", "label": "None of the above"}
            ]},
            {"id": "stress_level", "type": "scale", "label": "On a scale of 1-10, how would you rate your stress level?", "required": True, "min": 1, "max": 10, "labels": {1: "Very Low", 10: "Very High"}}
        ],
        "responses": {},
        "riskFactors": [
            {"category": "Lifestyle", "risk": "Medium", "factors": ["Sedentary lifestyle", "Poor diet quality"]},
            {"category": "Genetics", "risk": "Low", "factors": ["No significant family history"]}
        ],
        "recommendations": [
            "Increase physical activity to at least 150 minutes per week",
            "Focus on a balanced diet with more fruits and vegetables",
            "Consider stress management techniques like meditation",
            "Schedule regular health checkups"
        ]
    }
}

async def get_hra_step(mongo, user_id, step):
    doc = await mongo[DB_NAME]['hra'].find_one({"user_id": user_id})
    if not doc or "steps" not in doc:
        return None
    for s in doc["steps"]:
        if s.get("step") == step:
            return s
    return None

async def save_hra_step(mongo, user_id, step, step_data):
    # Ensure step_data always has the step field
    step_data = dict(step_data)
    step_data["step"] = step
    doc = await mongo[DB_NAME]['hra'].find_one({"user_id": user_id})
    if not doc or "steps" not in doc:
        steps = [step_data]
    else:
        steps = doc["steps"]
        updated = False
        for idx, s in enumerate(steps):
            if s.get("step") == step:
                steps[idx] = step_data
                updated = True
                break
        if not updated:
            steps.append(step_data)
    await mongo[DB_NAME]['hra'].update_one(
        {"user_id": user_id},
        {"$set": {"steps": steps}},
        upsert=True
    )
    return {"success": True, "nextStep": step + 1}

async def get_hra_report(mongo, user_id):
    doc = await mongo[DB_NAME]['hra'].find_one({"user_id": user_id})
    return doc.get("report", {}) if doc else None 