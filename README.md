# Health & Wellness Platform - Backend API

A comprehensive health and wellness platform backend built with **Sanic** and **MongoDB**. This service provides RESTful APIs for user profile management, health tracking, goal setting, and wellness assessments.

## 🏗️ Architecture

- **Framework**: Sanic (Async Python web framework)
- **Database**: MongoDB Atlas
- **API Version**: v2
- **Authentication**: User-based (via user_id parameter)

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- MongoDB Atlas account
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Premmakwana1/hackathon_1mg.git
   cd hackathon_1mg
   ```

2. **Install dependencies**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure MongoDB**
   - The application is pre-configured to connect to MongoDB Atlas
   - Database credentials are set in `backend/config.json`
   - Database: `launchpad`
   - Collections: `user`, `profile`, `activity_tracker`, `hra`, `search`

4. **Start the server**
   ```bash
   python app.py
   ```

The server will start on `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/v2/api
```

### Authentication
All endpoints require a `user_id` parameter (either as query parameter or in the request body).

### Available Endpoints

#### 🏠 Home Dashboard
```http
GET /home?user_id={user_id}
```
Returns user's home dashboard data including stats, recent activities, and progress.

#### 👤 Profile Management
```http
GET /profile/basic/{step}?user_id={user_id}
POST /profile/basic/{step}/save?user_id={user_id}
```
Manage user profile information across multiple steps.

**Example POST:**
```json
{
  "age": 30,
  "gender": "male",
  "height": 175,
  "weight": 70
}
```

#### 🎯 Goals Management
```http
GET /goals/{step}?user_id={user_id}
POST /goals/{step}/save?user_id={user_id}
```
Set and manage user health and wellness goals.

**Example POST:**
```json
{
  "goal": "weight_loss",
  "target": 65,
  "timeline": "3_months"
}
```

#### 🚀 Onboarding
```http
GET /onboarding/{step}?user_id={user_id}
POST /onboarding/{step}/save?user_id={user_id}
```
Handle user onboarding flow across multiple steps.

**Example POST:**
```json
{
  "welcome": true,
  "terms_accepted": true
}
```

#### 📊 Activity Tracking
```http
POST /activity/log?user_id={user_id}
GET /activity/dashboard?user_id={user_id}
POST /activity/goals/update?user_id={user_id}
```
Log activities and view activity dashboard.

**Example Activity Log:**
```json
{
  "activity": "walking",
  "duration": 30,
  "calories": 150,
  "steps": 3000
}
```

#### 🏃‍♂️ Trackers
```http
GET /trackers/{step}?user_id={user_id}
POST /trackers/{step}/save?user_id={user_id}
```
Manage different health trackers (steps, water, sleep, etc.).

**Example POST:**
```json
{
  "tracker": "steps",
  "enabled": true,
  "daily_goal": 10000
}
```

#### 🏥 Health Risk Assessment (HRA)
```http
GET /hra/{step}?user_id={user_id}
POST /hra/{step}/save?user_id={user_id}
GET /hra/report?user_id={user_id}
```
Complete health risk assessments and view reports.

**Example HRA Response:**
```json
{
  "question": "health_status",
  "answer": "good",
  "risk_score": 25
}
```

#### 🔍 Search
```http
GET /search?user_id={user_id}
POST /search/query
```
Search for health content, exercises, and wellness information.

**Example Search:**
```json
{
  "query": "cardio exercises",
  "filters": {
    "category": "exercise",
    "duration": "30_min"
  }
}
```

#### 🧭 Navigation
```http
POST /navigation/save-continue?user_id={user_id}
POST /navigation/save-exit?user_id={user_id}
```
Handle user navigation flow and progress saving.

**Example Continue:**
```json
{
  "currentStep": 1,
  "action": "continue",
  "progress": 25
}
```

#### 📈 User Progress
```http
GET /user/progress?user_id={user_id}
POST /user/progress/update?user_id={user_id}
```
Track and update user progress across different modules.

**Example Progress Update:**
```json
{
  "step": 1,
  "completed": true,
  "score": 85
}
```

#### 🌟 Wellness
```http
GET /wellness/intro?user_id={user_id}
```
Access wellness content and recommendations.

## 🗄️ Database Schema

### Collections

1. **`user`** - User profiles and preferences
2. **`profile`** - Detailed user profile information
3. **`activity_tracker`** - Activity logs and goals
4. **`hra`** - Health risk assessment data
5. **`search`** - Searchable content and suggestions

### Sample Document Structure

**User Profile:**
```json
{
  "user_id": "1",
  "profile": {
    "steps": [
      {
        "step": 1,
        "questions": [...],
        "userResponses": {
          "age": 30,
          "gender": "male"
        },
        "validationErrors": {}
      }
    ]
  }
}
```

**Activity Log:**
```json
{
  "user_id": "1",
  "activities": [
    {
      "activity": "walking",
      "duration": 30,
      "timestamp": "2024-01-15T10:00:00Z"
    }
  ],
  "goals": {
    "steps": 10000,
    "calories": 2000
  }
}
```

## 🧪 Testing

### Test the API

1. **Start the server**
   ```bash
   cd backend
   python app.py
   ```

2. **Test endpoints**
   ```bash
   # Test profile endpoint
   curl -X POST "http://localhost:8000/v2/api/profile/basic/1/save?user_id=1" \
     -H "Content-Type: application/json" \
     -d '{"age": 30, "gender": "male"}'

   # Test activity logging
   curl -X POST "http://localhost:8000/v2/api/activity/log?user_id=1" \
     -H "Content-Type: application/json" \
     -d '{"activity": "walking", "duration": 30}'

   # Test home dashboard
   curl -X GET "http://localhost:8000/v2/api/home?user_id=1"
   ```

## 🔧 Configuration

### Environment Variables
The application supports the following environment variables:

- `MONGO_DB_NAME` - Database name (default: launchpad)
- `MONGO_HOSTS` - MongoDB hosts
- `MONGO_USER` - MongoDB username
- `MONGO_PASS` - MongoDB password

### Config File
Main configuration is in `backend/config.json`:
```json
{
  "NAME": "launchpad-backend",
  "HOST": "0.0.0.0",
  "PORT": 8000,
  "DEBUG": true,
  "API_VERSION": "v2",
  "MONGO": {
    "DB_NAME": "launchpad",
    "HOSTS": ["launchpad.rpikq1h.mongodb.net"],
    "USER": "premmakwana",
    "PASS": "your_password_here"
  }
}
```

## 📁 Project Structure

```
hackathon_1mg/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── v2/              # API routes
│   │   │       ├── profile.py
│   │   │       ├── goals.py
│   │   │       ├── onboarding.py
│   │   │       ├── activity.py
│   │   │       ├── trackers.py
│   │   │       ├── hra.py
│   │   │       ├── search.py
│   │   │       ├── navigation.py
│   │   │       ├── user_progress.py
│   │   │       ├── wellness.py
│   │   │       └── home.py
│   │   ├── services/            # Business logic
│   │   ├── models/              # Data models
│   │   └── db/                  # Database configuration
│   ├── config.json              # Configuration
│   ├── requirements.txt         # Dependencies
│   └── app.py                   # Main application
├── api/                         # Mock data and templates
└── README.md                    # This file
```

## 🚀 Deployment

### Production Setup

1. **Environment Variables**
   ```bash
   export MONGO_PASSWORD=your_secure_password
   export MONGO_DB_NAME=launchpad_prod
   ```

2. **Security**
   - Enable HTTPS
   - Set up MongoDB Atlas IP whitelist
   - Use environment variables for sensitive data

3. **Performance**
   - Enable MongoDB connection pooling
   - Set up proper logging
   - Configure monitoring

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the 1MG Hackathon.

## 🆘 Support

For issues and questions:
- Check the API documentation above
- Review the database schema
- Test with the provided curl examples
- Check server logs for debugging information

---

**Happy Coding! 🚀** 