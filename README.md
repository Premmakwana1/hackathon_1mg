# Hackathon 1MG - Health & Wellness Platform

A comprehensive health and wellness platform with backend APIs built using Sanic and MongoDB.

## 🚨 **SECURITY ALERT**

**IMPORTANT**: The MongoDB password has been exposed in logs. Please follow these steps immediately:

1. **Change MongoDB Password**: 
   - Go to MongoDB Atlas Dashboard → Database Access
   - Change password for user `premmakwana`
   - Update your environment variables

2. **Use Environment Variables**: Never hardcode passwords in config files

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB Atlas account
- Git

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd hackathon_1mg
   ```

2. **Set up environment variables**
   ```bash
   cd backend
   cp env.example .env
   # Edit .env and add your MongoDB password
   export MONGO_PASSWORD=your_new_mongodb_password
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the server**
   ```bash
   python app.py
   ```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/v2/api
```

### Available Endpoints

#### Profile Management
- `GET /profile/basic/{step}?user_id={id}` - Get profile step
- `POST /profile/basic/{step}/save?user_id={id}` - Save profile step

#### Goals Management
- `GET /goals/{step}?user_id={id}` - Get goals step
- `POST /goals/{step}/save?user_id={id}` - Save goals step

#### Onboarding
- `GET /onboarding/{step}?user_id={id}` - Get onboarding step
- `POST /onboarding/{step}/save?user_id={id}` - Save onboarding step

#### Trackers
- `GET /trackers/{step}?user_id={id}` - Get tracker step
- `POST /trackers/{step}/save?user_id={id}` - Save tracker step

#### HRA (Health Risk Assessment)
- `GET /hra/{step}?user_id={id}` - Get HRA step
- `POST /hra/{step}/save?user_id={id}` - Save HRA step
- `GET /hra/report?user_id={id}` - Get HRA report

#### Activity Management
- `POST /activity/log?user_id={id}` - Log activity
- `GET /activity/dashboard?user_id={id}` - Get activity dashboard
- `POST /activity/goals/update?user_id={id}` - Update activity goals

#### Search
- `GET /search?user_id={id}` - Get search suggestions
- `POST /search/query` - Search query

#### Navigation
- `POST /navigation/save-continue?user_id={id}` - Save and continue
- `POST /navigation/save-exit?user_id={id}` - Save and exit

#### User Progress
- `GET /user/progress?user_id={id}` - Get user progress
- `POST /user/progress/update?user_id={id}` - Update user progress

#### Wellness
- `GET /wellness/intro?user_id={id}` - Get wellness intro

#### Home
- `GET /home?user_id={id}` - Get home data

## 🔧 Configuration

### Environment Variables
- `MONGO_PASSWORD` - MongoDB password (REQUIRED)
- `MONGO_DB_NAME` - Database name (default: launchpad)
- `MONGO_HOSTS` - MongoDB hosts (default: launchpad.rpikq1h.mongodb.net)
- `MONGO_USER` - MongoDB username (default: premmakwana)

### Config File
The `config.json` file contains default configuration. Environment variables will override these settings.

## 🛡️ Security Best Practices

1. **Never commit passwords** to version control
2. **Use environment variables** for sensitive data
3. **Regularly rotate** database passwords
4. **Enable MongoDB Atlas** security features (IP whitelist, etc.)
5. **Use HTTPS** in production

## 🧪 Testing

All endpoints have been tested and are working with MongoDB CRUD operations:

```bash
# Test profile endpoint
curl -X POST "http://localhost:8000/v2/api/profile/basic/1/save?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "gender": "male"}'

# Test activity logging
curl -X POST "http://localhost:8000/v2/api/activity/log?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{"activity": "walking", "duration": 30}'
```

## 📁 Project Structure

```
hackathon_1mg/
├── backend/
│   ├── app/
│   │   ├── routes/v2/          # API routes
│   │   ├── services/           # Business logic
│   │   ├── models/             # Data models
│   │   └── db/                 # Database configuration
│   ├── config.json             # Configuration
│   ├── requirements.txt        # Dependencies
│   └── app.py                  # Main application
├── api/                        # Mock data and templates
└── README.md                   # This file
```

## 🚀 Production Deployment

1. Set up environment variables in your deployment platform
2. Configure MongoDB Atlas for production access
3. Enable HTTPS and security headers
4. Set up monitoring and logging
5. Configure backup strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the 1MG Hackathon.