"""
Fallback service that provides v1 mock data when v2 APIs fail or return empty responses.
This ensures the frontend always gets data even if the database is unavailable.
"""

from sanic import response
from typing import Dict, Any, Optional

class FallbackService:
    """Service to provide fallback mock data when v2 APIs fail"""
    
    @staticmethod
    def get_home_fallback(user_id: str) -> Dict[str, Any]:
        """Fallback data for home endpoint"""
        return {
            "userName": "John Doe",
            "healthScore": 85,
            "dailyGoals": [
                {"id": 1, "title": "Steps", "current": 7500, "target": 10000, "unit": "steps", "progress": 75},
                {"id": 2, "title": "Water Intake", "current": 6, "target": 8, "unit": "glasses", "progress": 75},
                {"id": 3, "title": "Sleep", "current": 7, "target": 8, "unit": "hours", "progress": 87.5}
            ],
            "recentActivities": [
                {"id": 1, "type": "exercise", "title": "Morning Walk", "duration": "30 mins", "timestamp": "2025-06-26T06:30:00Z"},
                {"id": 2, "type": "meal", "title": "Healthy Breakfast", "calories": 350, "timestamp": "2025-06-26T08:00:00Z"}
            ],
            "upcomingAppointments": [
                {"id": 1, "type": "doctor", "title": "Annual Checkup", "date": "2025-06-28", "time": "10:00 AM", "doctor": "Dr. Smith"}
            ]
        }

    @staticmethod
    def get_profile_fallback(step: int) -> Optional[Dict[str, Any]]:
        """Fallback data for profile endpoint"""
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
        return PROFILE_MOCK.get(step)

    @staticmethod
    def get_goals_fallback(step: int) -> Optional[Dict[str, Any]]:
        """Fallback data for goals endpoint"""
        GOALS_MOCK = {
            1: {
                "step": 1,
                "title": "Set Your Health Goals",
                "description": "Choose your primary health goal",
                "options": [
                    {"id": "weight_loss", "title": "Weight Loss", "icon": "scale", "description": "Lose weight and get fit"},
                    {"id": "muscle_gain", "title": "Muscle Gain", "icon": "dumbbell", "description": "Build muscle and strength"},
                    {"id": "general_fitness", "title": "General Fitness", "icon": "heart", "description": "Improve overall fitness"},
                    {"id": "stress_management", "title": "Stress Management", "icon": "leaf", "description": "Reduce stress and anxiety"}
                ],
                "userResponses": {},
                "validationErrors": {}
            },
            2: {
                "step": 2,
                "title": "Set Your Target",
                "description": "Define your specific target",
                "questions": [
                    {"id": "target", "type": "number", "label": "What's your target?", "placeholder": "Enter your target", "required": True},
                    {"id": "timeline", "type": "select", "label": "Timeline", "required": True, "options": [
                        {"value": "1_month", "label": "1 Month"},
                        {"value": "3_months", "label": "3 Months"},
                        {"value": "6_months", "label": "6 Months"},
                        {"value": "1_year", "label": "1 Year"}
                    ]}
                ],
                "userResponses": {},
                "validationErrors": {}
            }
        }
        return GOALS_MOCK.get(step)

    @staticmethod
    def get_onboarding_fallback(step: int) -> Optional[Dict[str, Any]]:
        """Fallback data for onboarding endpoint"""
        ONBOARDING_MOCK = {
            1: {
                "step": 1,
                "title": "Welcome to Your Health Journey",
                "description": "Let's get started with your personalized health plan",
                "content": [
                    {"type": "text", "text": "We're excited to help you achieve your health goals!"},
                    {"type": "image", "url": "welcome_image.png", "alt": "Welcome"}
                ],
                "actions": [
                    {"id": "welcome", "type": "button", "label": "Get Started", "action": "continue"}
                ],
                "userResponses": {},
                "validationErrors": {}
            },
            2: {
                "step": 2,
                "title": "Terms & Conditions",
                "description": "Please review and accept our terms",
                "content": [
                    {"type": "text", "text": "By continuing, you agree to our terms of service and privacy policy."}
                ],
                "actions": [
                    {"id": "terms_accepted", "type": "checkbox", "label": "I accept the terms and conditions", "required": True}
                ],
                "userResponses": {},
                "validationErrors": {}
            }
        }
        return ONBOARDING_MOCK.get(step)

    @staticmethod
    def get_trackers_fallback(step: int) -> Optional[Dict[str, Any]]:
        """Fallback data for trackers endpoint"""
        TRACKERS_MOCK = {
            1: {
                "step": 1,
                "title": "Choose Your Trackers",
                "description": "Select the health metrics you want to track",
                "trackers": [
                    {"id": "steps", "title": "Steps", "icon": "footprints", "description": "Track daily step count", "enabled": True},
                    {"id": "water", "title": "Water Intake", "icon": "droplet", "description": "Track water consumption", "enabled": True},
                    {"id": "sleep", "title": "Sleep", "icon": "moon", "description": "Track sleep duration", "enabled": False},
                    {"id": "weight", "title": "Weight", "icon": "scale", "description": "Track weight changes", "enabled": False},
                    {"id": "meditation", "title": "Meditation", "icon": "lotus", "description": "Track meditation sessions", "enabled": False}
                ],
                "userResponses": {},
                "validationErrors": {}
            }
        }
        return TRACKERS_MOCK.get(step)

    @staticmethod
    def get_hra_fallback(step: int) -> Optional[Dict[str, Any]]:
        """Fallback data for HRA endpoint"""
        HRA_MOCK = {
            1: {
                "step": 1,
                "title": "Health Risk Assessment",
                "description": "Let's assess your current health status",
                "questions": [
                    {"id": "health_status", "type": "radio", "label": "How would you rate your overall health?", "required": True, "options": [
                        {"value": "excellent", "label": "Excellent"},
                        {"value": "good", "label": "Good"},
                        {"value": "fair", "label": "Fair"},
                        {"value": "poor", "label": "Poor"}
                    ]},
                    {"id": "exercise_frequency", "type": "radio", "label": "How often do you exercise?", "required": True, "options": [
                        {"value": "daily", "label": "Daily"},
                        {"value": "3_5_times", "label": "3-5 times per week"},
                        {"value": "1_2_times", "label": "1-2 times per week"},
                        {"value": "rarely", "label": "Rarely or never"}
                    ]}
                ],
                "userResponses": {},
                "validationErrors": {}
            }
        }
        return HRA_MOCK.get(step)

    @staticmethod
    def get_activity_fallback() -> Dict[str, Any]:
        """Fallback data for activity endpoint"""
        return {
            "todayStats": {
                "steps": 7500,
                "calories": 1200,
                "activeMinutes": 45,
                "waterGlasses": 6
            },
            "weeklyStats": {
                "totalSteps": 52000,
                "totalCalories": 8400,
                "totalActiveMinutes": 315,
                "averageWaterGlasses": 7
            },
            "activities": [
                {"id": 1, "activity": "walking", "duration": 30, "calories": 150, "timestamp": "2025-06-26T06:30:00Z"},
                {"id": 2, "activity": "yoga", "duration": 20, "calories": 80, "timestamp": "2025-06-26T18:00:00Z"}
            ],
            "goals": {
                "steps": 10000,
                "calories": 2000,
                "activeMinutes": 60,
                "waterGlasses": 8
            },
            "achievements": [
                {"id": 1, "title": "First Steps", "description": "Completed your first activity", "icon": "trophy", "unlocked": True},
                {"id": 2, "title": "Week Warrior", "description": "Completed 5 activities this week", "icon": "medal", "unlocked": False}
            ]
        }

    @staticmethod
    def get_search_fallback() -> Dict[str, Any]:
        """Fallback data for search endpoint"""
        return {
            "suggestions": ["Weight loss exercises", "Healthy breakfast recipes", "Stress management techniques"],
            "popularSearches": ["cardio workout", "meditation", "protein recipes"],
            "filters": {
                "categories": ["All", "Exercise", "Nutrition", "Wellness"],
                "difficulty": ["All", "Beginner", "Intermediate", "Advanced"],
                "duration": ["All", "10-30 min", "30-60 min", "60+ min"]
            }
        }

    @staticmethod
    def get_search_results_fallback(query: str) -> Dict[str, Any]:
        """Fallback data for search results"""
        return {
            "results": [
                {"id": 1, "type": "exercise", "title": "Push-ups", "description": "Chest and arm strengthening exercise", "duration": "10 min", "difficulty": "Beginner"},
                {"id": 2, "type": "recipe", "title": "Protein Smoothie", "description": "High-protein breakfast smoothie", "prepTime": "5 min", "calories": 250},
                {"id": 3, "type": "article", "title": "Benefits of Walking", "description": "Why walking is great for your health", "readTime": "3 min", "category": "Wellness"}
            ],
            "totalCount": 3,
            "suggestions": ["Try yoga", "Healthy snacks", "Morning routine"]
        }

    @staticmethod
    def get_navigation_fallback() -> Dict[str, Any]:
        """Fallback data for navigation endpoint"""
        return {
            "success": True,
            "nextRoute": "/goals/1",
            "nextStep": 2,
            "message": "Progress saved successfully"
        }

    @staticmethod
    def get_user_progress_fallback() -> Dict[str, Any]:
        """Fallback data for user progress endpoint"""
        return {
            "overallProgress": 65,
            "completedSteps": [1, 2, 3],
            "currentStep": 4,
            "totalSteps": 6,
            "modules": [
                {"id": "profile", "name": "Profile Setup", "progress": 100, "completed": True},
                {"id": "goals", "name": "Goal Setting", "progress": 75, "completed": False},
                {"id": "trackers", "name": "Tracker Selection", "progress": 50, "completed": False},
                {"id": "hra", "name": "Health Assessment", "progress": 0, "completed": False}
            ]
        }

    @staticmethod
    def get_wellness_fallback() -> Dict[str, Any]:
        """Fallback data for wellness endpoint"""
        return {
            "title": "Welcome to Wellness",
            "description": "Your journey to better health starts here",
            "features": [
                {"id": 1, "title": "Personalized Plans", "description": "Get customized health plans based on your goals", "icon": "target"},
                {"id": 2, "title": "Track Progress", "description": "Monitor your health metrics and achievements", "icon": "chart"},
                {"id": 3, "title": "Expert Guidance", "description": "Access to health experts and resources", "icon": "user-md"}
            ],
            "quickActions": [
                {"id": 1, "title": "Start Assessment", "action": "hra", "icon": "clipboard"},
                {"id": 2, "title": "Set Goals", "action": "goals", "icon": "flag"},
                {"id": 3, "title": "Track Activity", "action": "activity", "icon": "activity"}
            ]
        }

    @staticmethod
    def should_fallback(result: Any, error: Optional[Exception] = None) -> bool:
        """Determine if we should fall back to mock data"""
        if error:
            return True
        
        if result is None:
            return True
        
        if isinstance(result, dict):
            # Check if result is empty or contains error
            if not result or "error" in result:
                return True
            
            # Check if result is empty (no meaningful data)
            if len(result) == 0:
                return True
        
        return False

    @staticmethod
    def get_fallback_response(endpoint: str, **kwargs) -> Dict[str, Any]:
        """Get fallback response for any endpoint"""
        fallback_methods = {
            "home": FallbackService.get_home_fallback,
            "profile": FallbackService.get_profile_fallback,
            "goals": FallbackService.get_goals_fallback,
            "onboarding": FallbackService.get_onboarding_fallback,
            "trackers": FallbackService.get_trackers_fallback,
            "hra": FallbackService.get_hra_fallback,
            "activity": FallbackService.get_activity_fallback,
            "search": FallbackService.get_search_fallback,
            "search_results": FallbackService.get_search_results_fallback,
            "navigation": FallbackService.get_navigation_fallback,
            "user_progress": FallbackService.get_user_progress_fallback,
            "wellness": FallbackService.get_wellness_fallback
        }
        
        method = fallback_methods.get(endpoint)
        if method:
            return method(**kwargs)
        
        return {"error": "Fallback data not available for this endpoint"}

    @staticmethod
    def get_activity_dashboard_fallback() -> Dict[str, Any]:
        """Fallback data for activity dashboard endpoint"""
        return FallbackService.get_activity_fallback()

    @staticmethod
    def get_activity_log_fallback() -> Dict[str, Any]:
        """Fallback data for activity log endpoint"""
        return {
            "success": True,
            "activityId": "mock_activity_123",
            "_fallback": True
        }

    @staticmethod
    def get_activity_goals_fallback() -> Dict[str, Any]:
        """Fallback data for activity goals update endpoint"""
        return {
            "success": True,
            "updatedGoals": {
                "steps": 10000,
                "calories": 2000,
                "activeMinutes": 60
            },
            "_fallback": True
        }

    @staticmethod
    def get_search_suggestions_fallback() -> Dict[str, Any]:
        """Fallback data for search suggestions endpoint"""
        return FallbackService.get_search_fallback()

    @staticmethod
    def get_search_results_fallback_with_query(query: str = "") -> Dict[str, Any]:
        """Fallback data for search results endpoint"""
        return FallbackService.get_search_results_fallback(query)

    @staticmethod
    def get_navigation_continue_fallback() -> Dict[str, Any]:
        """Fallback data for navigation save-continue endpoint"""
        return {
            "success": True,
            "nextRoute": "/goals/1",
            "nextStep": 2,
            "message": "Progress saved successfully",
            "_fallback": True
        }

    @staticmethod
    def get_navigation_exit_fallback() -> Dict[str, Any]:
        """Fallback data for navigation save-exit endpoint"""
        return {
            "success": True,
            "resumeToken": "mock_token_123",
            "message": "Progress saved, you can resume later",
            "_fallback": True
        }

    @staticmethod
    def get_user_progress_update_fallback() -> Dict[str, Any]:
        """Fallback data for user progress update endpoint"""
        return {
            "success": True,
            "updatedProgress": {
                "step": 1,
                "completed": True,
                "score": 85
            },
            "_fallback": True
        }

    @staticmethod
    def get_wellness_intro_fallback() -> Dict[str, Any]:
        """Fallback data for wellness intro endpoint"""
        return FallbackService.get_wellness_fallback()

    @staticmethod
    def get_hra_report_fallback() -> Dict[str, Any]:
        """Fallback data for HRA report endpoint"""
        return {
            "reportId": "mock_report_123",
            "generatedAt": "2025-01-15T10:00:00Z",
            "riskScore": 25,
            "riskLevel": "Low",
            "recommendations": [
                "Continue with your current healthy lifestyle",
                "Consider adding more cardiovascular exercise",
                "Maintain regular health checkups"
            ],
            "summary": "Your health assessment shows good overall health with room for improvement in cardiovascular fitness.",
            "_fallback": True
        } 