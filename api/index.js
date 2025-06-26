/**
 * API Module Exports
 * Central export file for all API-related utilities
 */

// API Endpoints and Configuration
export { API_ENDPOINTS, API_CONFIG, getEndpoint } from './apiEndpoints'

// Mock Data Mapping
export { 
    API_MOCK_MAPPING, 
    COMPONENT_API_MAPPING, 
    POST_RESPONSE_TEMPLATES,
    getMockDataForEndpoint,
    generatePostResponse 
} from './apiMockDataMapping'

// API Service
export { default as apiService, ApiService } from '../services/apiService'

// Re-export mock data for convenience
export {
    homePageMockData,
    onboardingMockData,
    basicProfileMockData,
    goalSelectMockData,
    trackerSelectionMockData,
    hraMockData,
    activityTrackerMockData,
    searchMockData,
    wellnessMockData,
    getMockData
} from '../mockData'

// API Usage Examples and Documentation
export const API_USAGE_EXAMPLES = {
    // How to use in components
    component_example: `
    import { apiService } from '@api'
    
    // In component
    const fetchData = async () => {
        try {
            const data = await apiService.getOnboardingStep(1)
            setPageData(data)
        } catch (error) {
            console.error('Failed to fetch data:', error)
        }
    }
    
    const saveData = async (formData) => {
        try {
            const response = await apiService.saveOnboardingStep(1, formData)
            if (response.success) {
                navigate(response.nextRoute)
            }
        } catch (error) {
            console.error('Failed to save data:', error)
        }
    }
    `,
    
    // How to add new endpoints
    add_endpoint_example: `
    // 1. Add to apiEndpoints.js
    NEW_FEATURE: {
        GET: {
            endpoint: '/api/v1/new-feature',
            method: 'GET',
            description: 'Get new feature data',
            mockData: 'newFeatureMockData'
        }
    }
    
    // 2. Add mock data to mockData folder
    // 3. Add to apiMockDataMapping.js
    // 4. Add method to apiService.js
    `
}

// API Health Check
export const checkApiHealth = async () => {
    try {
        const response = await fetch(`${API_CONFIG.baseURL}/health`)
        return response.status === 200
    } catch (error) {
        return false
    }
}