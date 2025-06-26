/**
 * API Endpoints Specification for Health Engagement App
 * This file lists all required APIs with their corresponding mock data
 */

export const API_ENDPOINTS = {
    
    // ===========================================
    // HOME PAGE APIs
    // ===========================================
    HOME_PAGE: {
        GET: {
            endpoint: '/api/v1/home',
            method: 'GET',
            description: 'Get user dashboard data including health score, goals, activities',
            mockData: 'homePageMockData',
            response: {
                userName: 'string',
                healthScore: 'number',
                dailyGoals: 'array',
                recentActivities: 'array',
                upcomingAppointments: 'array'
            }
        }
    },

    // ===========================================
    // WELCOME TO WELLNESS APIs
    // ===========================================
    WELLNESS: {
        GET: {
            endpoint: '/api/v1/wellness/intro',
            method: 'GET',
            description: 'Get wellness introduction page content',
            mockData: 'wellnessMockData',
            response: {
                welcomeMessage: 'string',
                benefits: 'array',
                features: 'array',
                testimonials: 'array'
            }
        }
    },

    // ===========================================
    // ONBOARDING APIs
    // ===========================================
    ONBOARDING: {
        GET: {
            endpoint: '/api/v1/onboarding/:step',
            method: 'GET',
            description: 'Get onboarding step data and options',
            mockData: 'onboardingMockData.step{n}',
            pathParams: ['step'],
            response: {
                step: 'number',
                totalSteps: 'number',
                title: 'string',
                description: 'string',
                options: 'array'
            }
        },
        POST: {
            endpoint: '/api/v1/onboarding/:step/save',
            method: 'POST',
            description: 'Save onboarding step response and navigate to next step',
            pathParams: ['step'],
            requestBody: {
                selectedOptions: 'array',
                userResponse: 'object'
            },
            response: {
                success: 'boolean',
                nextStep: 'number',
                message: 'string'
            }
        }
    },

    // ===========================================
    // BASIC PROFILE APIs
    // ===========================================
    BASIC_PROFILE: {
        GET: {
            endpoint: '/api/v1/profile/basic/:step',
            method: 'GET',
            description: 'Get basic profile form questions for specific step',
            mockData: 'basicProfileMockData.step{n}',
            pathParams: ['step'],
            response: {
                step: 'number',
                questions: 'array',
                userResponses: 'object',
                validationErrors: 'object'
            }
        },
        POST: {
            endpoint: '/api/v1/profile/basic/:step/save',
            method: 'POST',
            description: 'Save basic profile data for current step',
            pathParams: ['step'],
            requestBody: {
                responses: 'object',
                isComplete: 'boolean'
            },
            response: {
                success: 'boolean',
                validationErrors: 'object',
                nextStep: 'number'
            }
        }
    },

    // ===========================================
    // GOAL SELECTION APIs
    // ===========================================
    GOAL_SELECT: {
        GET: {
            endpoint: '/api/v1/goals/:step',
            method: 'GET',
            description: 'Get available goals and recommendations for selection',
            mockData: 'goalSelectMockData.step{n}',
            pathParams: ['step'],
            response: {
                step: 'number',
                availableGoals: 'array',
                selectedGoals: 'array',
                recommendations: 'array'
            }
        },
        POST: {
            endpoint: '/api/v1/goals/:step/save',
            method: 'POST',
            description: 'Save selected goals and get personalized recommendations',
            pathParams: ['step'],
            requestBody: {
                selectedGoals: 'array',
                preferences: 'object'
            },
            response: {
                success: 'boolean',
                recommendations: 'array',
                nextStep: 'number'
            }
        }
    },

    // ===========================================
    // TRACKER SELECTION APIs
    // ===========================================
    TRACKER_SELECTION: {
        GET: {
            endpoint: '/api/v1/trackers/:step',
            method: 'GET',
            description: 'Get available health trackers by category',
            mockData: 'trackerSelectionMockData.step{n}',
            pathParams: ['step'],
            response: {
                step: 'number',
                categories: 'array',
                availableTrackers: 'array',
                selectedTrackers: 'array'
            }
        },
        POST: {
            endpoint: '/api/v1/trackers/:step/save',
            method: 'POST',
            description: 'Save selected trackers and configure default goals',
            pathParams: ['step'],
            requestBody: {
                selectedTrackers: 'array',
                trackerConfigs: 'object'
            },
            response: {
                success: 'boolean',
                configuredTrackers: 'array',
                nextStep: 'number'
            }
        }
    },

    // ===========================================
    // HEALTH RISK ASSESSMENT APIs
    // ===========================================
    HRA: {
        GET: {
            endpoint: '/api/v1/hra/:step',
            method: 'GET',
            description: 'Get HRA questions and assessment data',
            mockData: 'hraMockData.step{n}',
            pathParams: ['step'],
            response: {
                step: 'number',
                questions: 'array',
                responses: 'object',
                riskFactors: 'array',
                recommendations: 'array'
            }
        },
        POST: {
            endpoint: '/api/v1/hra/:step/save',
            method: 'POST',
            description: 'Save HRA responses and calculate risk assessment',
            pathParams: ['step'],
            requestBody: {
                responses: 'object',
                isComplete: 'boolean'
            },
            response: {
                success: 'boolean',
                riskAssessment: 'object',
                recommendations: 'array',
                nextStep: 'number'
            }
        },
        GET_REPORT: {
            endpoint: '/api/v1/hra/report',
            method: 'GET',
            description: 'Get complete HRA report with risk analysis',
            response: {
                overallRisk: 'string',
                riskFactors: 'array',
                recommendations: 'array',
                nextSteps: 'array'
            }
        }
    },

    // ===========================================
    // ACTIVITY TRACKER APIs
    // ===========================================
    ACTIVITY_TRACKER: {
        GET: {
            endpoint: '/api/v1/activity/dashboard',
            method: 'GET',
            description: 'Get activity tracking dashboard with stats and goals',
            mockData: 'activityTrackerMockData',
            response: {
                todayStats: 'object',
                weeklyStats: 'object',
                activities: 'array',
                goals: 'object',
                achievements: 'array'
            }
        },
        POST_ACTIVITY: {
            endpoint: '/api/v1/activity/log',
            method: 'POST',
            description: 'Log new activity or update existing activity',
            requestBody: {
                type: 'string',
                title: 'string',
                duration: 'number',
                calories: 'number',
                intensity: 'string',
                timestamp: 'string'
            },
            response: {
                success: 'boolean',
                activityId: 'string',
                updatedStats: 'object'
            }
        },
        POST_GOALS: {
            endpoint: '/api/v1/activity/goals/update',
            method: 'POST',
            description: 'Update daily/weekly activity goals',
            requestBody: {
                dailyGoals: 'object',
                weeklyGoals: 'object'
            },
            response: {
                success: 'boolean',
                updatedGoals: 'object'
            }
        }
    },

    // ===========================================
    // SEARCH APIs
    // ===========================================
    SEARCH: {
        GET: {
            endpoint: '/api/v1/search',
            method: 'GET',
            description: 'Get search page data with suggestions and popular searches',
            mockData: 'searchMockData',
            response: {
                suggestions: 'array',
                popularSearches: 'array',
                filters: 'object'
            }
        },
        POST_SEARCH: {
            endpoint: '/api/v1/search/query',
            method: 'POST',
            description: 'Perform search query with filters',
            requestBody: {
                query: 'string',
                filters: 'object',
                page: 'number',
                limit: 'number'
            },
            response: {
                results: 'array',
                totalCount: 'number',
                suggestions: 'array'
            }
        }
    },

    // ===========================================
    // USER PROGRESS APIs
    // ===========================================
    USER_PROGRESS: {
        GET: {
            endpoint: '/api/v1/user/progress',
            method: 'GET',
            description: 'Get overall user progress across all modules',
            response: {
                completionStatus: 'object',
                currentStep: 'object',
                overallProgress: 'number'
            }
        },
        POST: {
            endpoint: '/api/v1/user/progress/update',
            method: 'POST',
            description: 'Update user progress when completing steps',
            requestBody: {
                module: 'string',
                step: 'number',
                completed: 'boolean',
                data: 'object'
            },
            response: {
                success: 'boolean',
                updatedProgress: 'object'
            }
        }
    },

    // ===========================================
    // NAVIGATION & STATE APIs
    // ===========================================
    NAVIGATION: {
        POST_SAVE_AND_CONTINUE: {
            endpoint: '/api/v1/navigation/save-continue',
            method: 'POST',
            description: 'Save current page data and get next navigation step',
            requestBody: {
                currentPage: 'string',
                currentStep: 'number',
                formData: 'object',
                navigationAction: 'string'
            },
            response: {
                success: 'boolean',
                nextRoute: 'string',
                nextStep: 'number',
                message: 'string'
            }
        },
        POST_SAVE_AND_EXIT: {
            endpoint: '/api/v1/navigation/save-exit',
            method: 'POST',
            description: 'Save current progress and allow user to exit/resume later',
            requestBody: {
                currentPage: 'string',
                currentStep: 'number',
                formData: 'object'
            },
            response: {
                success: 'boolean',
                resumeToken: 'string',
                message: 'string'
            }
        }
    }
}

// Helper function to get endpoint by component and action
export const getEndpoint = (component, action, step = null) => {
    const componentKey = component.toUpperCase().replace(/([A-Z])/g, '_$1').substring(1)
    const endpoint = API_ENDPOINTS[componentKey]
    
    if (!endpoint) return null
    
    let targetEndpoint = endpoint[action.toUpperCase()]
    if (targetEndpoint && step) {
        targetEndpoint = {
            ...targetEndpoint,
            endpoint: targetEndpoint.endpoint.replace(':step', step)
        }
    }
    
    return targetEndpoint
}

// API Base Configuration
export const API_CONFIG = {
    baseURL: process.env.REACT_APP_API_BASE_URL || 'http://localhost:3001',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
}