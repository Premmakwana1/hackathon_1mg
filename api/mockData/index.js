// Export all mock data
export { homePageMockData } from './homePageData'
export { onboardingMockData } from './onboardingData'
export { basicProfileMockData } from './basicProfileData'
export { goalSelectMockData } from './goalSelectData'
export { trackerSelectionMockData } from './trackerSelectionData'
export { hraMockData } from './hraData'
export { activityTrackerMockData } from './activityTrackerData'
export { searchMockData } from './searchData'
export { wellnessMockData } from './wellnessData'

// Utility function to get mock data by component and step
export const getMockData = (component, step = null) => {
    const dataMap = {
        'homePage': homePageMockData,
        'onboarding': step ? onboardingMockData[`step${step}`] : onboardingMockData,
        'basicProfile': step ? basicProfileMockData[`step${step}`] : basicProfileMockData,
        'goalSelect': step ? goalSelectMockData[`step${step}`] : goalSelectMockData,
        'trackerSelection': step ? trackerSelectionMockData[`step${step}`] : trackerSelectionMockData,
        'hra': step ? hraMockData[`step${step}`] : hraMockData,
        'activityTracker': activityTrackerMockData,
        'search': searchMockData,
        'wellness': wellnessMockData
    }
    
    return dataMap[component] || null
}