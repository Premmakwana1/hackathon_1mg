/**
 * API to Mock Data Mapping
 * This file maps each API endpoint to its corresponding mock data
 */

import { 
    homePageMockData,
    onboardingMockData,
    basicProfileMockData,
    goalSelectMockData,
    trackerSelectionMockData,
    hraMockData,
    activityTrackerMockData,
    searchMockData,
    wellnessMockData
} from '../mockData'

export const API_MOCK_MAPPING = {
    
    // Home Page APIs
    '/api/v1/home': {
        GET: homePageMockData
    },

    // Wellness APIs
    '/api/v1/wellness/intro': {
        GET: wellnessMockData
    },

    // Onboarding APIs
    '/api/v1/onboarding/1': {
        GET: onboardingMockData.step1
    },
    '/api/v1/onboarding/2': {
        GET: onboardingMockData.step2
    },
    '/api/v1/onboarding/3': {
        GET: onboardingMockData.step3
    },
    '/api/v1/onboarding/4': {
        GET: onboardingMockData.step4
    },
    '/api/v1/onboarding/5': {
        GET: onboardingMockData.step5
    },

    // Basic Profile APIs
    '/api/v1/profile/basic/1': {
        GET: basicProfileMockData.step1
    },
    '/api/v1/profile/basic/2': {
        GET: basicProfileMockData.step2
    },
    '/api/v1/profile/basic/3': {
        GET: basicProfileMockData.step3
    },

    // Goal Selection APIs
    '/api/v1/goals/1': {
        GET: goalSelectMockData.step1
    },
    '/api/v1/goals/2': {
        GET: goalSelectMockData.step2
    },

    // Tracker Selection APIs
    '/api/v1/trackers/1': {
        GET: trackerSelectionMockData.step1
    },
    '/api/v1/trackers/2': {
        GET: trackerSelectionMockData.step2
    },

    // HRA APIs
    '/api/v1/hra/1': {
        GET: hraMockData.step1
    },
    '/api/v1/hra/2': {
        GET: hraMockData.step2
    },
    '/api/v1/hra/3': {
        GET: hraMockData.step3
    },

    // Activity Tracker APIs
    '/api/v1/activity/dashboard': {
        GET: activityTrackerMockData
    },

    // Search APIs
    '/api/v1/search': {
        GET: searchMockData
    }
}

// Component to API mapping for easy reference
export const COMPONENT_API_MAPPING = {
    HomePage: {
        getData: '/api/v1/home',
        mockData: 'homePageMockData'
    },
    WelcomeToWellness: {
        getData: '/api/v1/wellness/intro',
        mockData: 'wellnessMockData'
    },
    OnboardingScreen: {
        getData: '/api/v1/onboarding/:step',
        saveData: '/api/v1/onboarding/:step/save',
        mockData: 'onboardingMockData.step{n}'
    },
    BasicProfile: {
        getData: '/api/v1/profile/basic/:step',
        saveData: '/api/v1/profile/basic/:step/save',
        mockData: 'basicProfileMockData.step{n}'
    },
    GoalSelect: {
        getData: '/api/v1/goals/:step',
        saveData: '/api/v1/goals/:step/save',
        mockData: 'goalSelectMockData.step{n}'
    },
    TrackerSelection: {
        getData: '/api/v1/trackers/:step',
        saveData: '/api/v1/trackers/:step/save',
        mockData: 'trackerSelectionMockData.step{n}'
    },
    HRA: {
        getData: '/api/v1/hra/:step',
        saveData: '/api/v1/hra/:step/save',
        getReport: '/api/v1/hra/report',
        mockData: 'hraMockData.step{n}'
    },
    ActivityTracker: {
        getData: '/api/v1/activity/dashboard',
        logActivity: '/api/v1/activity/log',
        updateGoals: '/api/v1/activity/goals/update',
        mockData: 'activityTrackerMockData'
    },
    SearchTab: {
        getData: '/api/v1/search',
        searchQuery: '/api/v1/search/query',
        mockData: 'searchMockData'
    }
}

// Mock response templates for POST requests
export const POST_RESPONSE_TEMPLATES = {
    success: {
        success: true,
        message: 'Data saved successfully',
        timestamp: new Date().toISOString()
    },
    error: {
        success: false,
        message: 'Failed to save data',
        errors: [],
        timestamp: new Date().toISOString()
    },
    validation: {
        success: false,
        message: 'Validation failed',
        validationErrors: {},
        timestamp: new Date().toISOString()
    },
    navigation: {
        success: true,
        nextRoute: '',
        nextStep: 1,
        message: 'Navigation successful'
    }
}

// Function to get mock data for any endpoint
export const getMockDataForEndpoint = (endpoint, method = 'GET') => {
    const mapping = API_MOCK_MAPPING[endpoint]
    return mapping ? mapping[method] : null
}

// Function to generate POST response based on request
export const generatePostResponse = (endpoint, requestData) => {
    // Simple validation simulation
    if (!requestData || Object.keys(requestData).length === 0) {
        return {
            ...POST_RESPONSE_TEMPLATES.validation,
            validationErrors: { general: 'Request data is required' }
        }
    }

    // Simulate successful save with next step logic
    if (endpoint.includes('/save')) {
        const stepMatch = endpoint.match(/\/(\d+)\/save/)
        const currentStep = stepMatch ? parseInt(stepMatch[1]) : 1
        
        return {
            ...POST_RESPONSE_TEMPLATES.navigation,
            nextStep: currentStep + 1,
            savedData: requestData
        }
    }

    return {
        ...POST_RESPONSE_TEMPLATES.success,
        savedData: requestData
    }
}