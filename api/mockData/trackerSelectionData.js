export const trackerSelectionMockData = {
    step1: {
        step: 1,
        categories: [
            {
                id: "fitness",
                title: "Fitness Trackers",
                description: "Monitor your physical activities"
            },
            {
                id: "health",
                title: "Health Monitors",
                description: "Track vital health metrics"
            },
            {
                id: "lifestyle",
                title: "Lifestyle Trackers",
                description: "Monitor daily habits and routines"
            }
        ],
        availableTrackers: [
            {
                id: "steps",
                title: "Step Counter",
                description: "Track daily steps and distance",
                category: "fitness",
                icon: "steps",
                enabled: true,
                defaultGoal: 10000
            },
            {
                id: "calories",
                title: "Calorie Tracker",
                description: "Monitor calories burned and consumed",
                category: "fitness",
                icon: "calories",
                enabled: false,
                defaultGoal: 2000
            },
            {
                id: "heart_rate",
                title: "Heart Rate Monitor",
                description: "Track resting and active heart rate",
                category: "health",
                icon: "heart",
                enabled: false,
                defaultGoal: 70
            },
            {
                id: "sleep",
                title: "Sleep Tracker",
                description: "Monitor sleep duration and quality",
                category: "lifestyle",
                icon: "sleep",
                enabled: true,
                defaultGoal: 8
            }
        ],
        selectedTrackers: ["steps", "sleep"]
    },
    step2: {
        step: 2,
        categories: [
            {
                id: "nutrition",
                title: "Nutrition Trackers",
                description: "Monitor your eating habits"
            },
            {
                id: "mental_health",
                title: "Mental Health",
                description: "Track mood and stress levels"
            }
        ],
        availableTrackers: [
            {
                id: "water_intake",
                title: "Water Intake",
                description: "Track daily water consumption",
                category: "nutrition",
                icon: "water",
                enabled: true,
                defaultGoal: 8
            },
            {
                id: "meal_log",
                title: "Meal Logger",
                description: "Log your meals and snacks",
                category: "nutrition",
                icon: "food",
                enabled: false,
                defaultGoal: 3
            },
            {
                id: "mood",
                title: "Mood Tracker",
                description: "Monitor daily mood and emotions",
                category: "mental_health",
                icon: "mood",
                enabled: false,
                defaultGoal: 1
            },
            {
                id: "meditation",
                title: "Meditation Timer",
                description: "Track meditation and mindfulness",
                category: "mental_health",
                icon: "meditation",
                enabled: false,
                defaultGoal: 10
            }
        ],
        selectedTrackers: ["water_intake"]
    }
}