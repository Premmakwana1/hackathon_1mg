from sanic import Blueprint, response, Request

wellness_bp = Blueprint('wellness', url_prefix='/wellness')

@wellness_bp.route('/intro')
async def wellness_intro_handler(request: Request):
    return response.json({
        "welcomeMessage": "Welcome to Your Wellness Journey",
        "subtitle": "Take control of your health with personalized insights and guidance",
        "benefits": [
            {"id": 1, "title": "Personalized Health Insights", "description": "Get tailored recommendations based on your unique health profile", "icon": "insights"},
            {"id": 2, "title": "Track Your Progress", "description": "Monitor your health metrics and see improvements over time", "icon": "progress"},
            {"id": 3, "title": "Expert Guidance", "description": "Access professional health advice and resources", "icon": "expert"},
            {"id": 4, "title": "Community Support", "description": "Connect with others on similar health journeys", "icon": "community"}
        ],
        "features": [
            {"id": 1, "title": "Health Risk Assessment", "description": "Comprehensive evaluation of your health risks", "image": "/images/hra.jpg"},
            {"id": 2, "title": "Activity Tracking", "description": "Monitor your daily activities and fitness goals", "image": "/images/activity.jpg"},
            {"id": 3, "title": "Nutrition Guidance", "description": "Personalized meal plans and nutrition advice", "image": "/images/nutrition.jpg"},
            {"id": 4, "title": "Mental Wellness", "description": "Tools for stress management and mental health", "image": "/images/mental.jpg"}
        ],
        "testimonials": [
            {"id": 1, "name": "Sarah Johnson", "role": "Fitness Enthusiast", "quote": "This app helped me achieve my fitness goals with personalized guidance.", "rating": 5, "image": "/images/user1.jpg"},
            {"id": 2, "name": "Michael Chen", "role": "Busy Professional", "quote": "Finally, a health app that fits into my busy schedule and actually works.", "rating": 5, "image": "/images/user2.jpg"},
            {"id": 3, "name": "Emma Davis", "role": "Health Coach", "quote": "I recommend this app to all my clients. The insights are incredibly valuable.", "rating": 5, "image": "/images/user3.jpg"}
        ],
        "ctaButtons": [
            {"id": 1, "text": "Start Your Journey", "type": "primary", "action": "navigate", "target": "/onboarding/1"},
            {"id": 2, "text": "Learn More", "type": "secondary", "action": "scroll", "target": "#features"}
        ]
    })

wellness_bp.add_route(wellness_intro_handler, '/intro') 