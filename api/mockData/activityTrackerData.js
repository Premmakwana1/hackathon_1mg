export const activityTrackerMockData = {
    todayStats: {
        steps: {
            current: 7500,
            goal: 10000,
            progress: 75,
            unit: "steps"
        },
        calories: {
            current: 1850,
            goal: 2200,
            progress: 84,
            unit: "kcal"
        },
        activeMinutes: {
            current: 45,
            goal: 60,
            progress: 75,
            unit: "minutes"
        },
        distance: {
            current: 5.2,
            goal: 7.0,
            progress: 74,
            unit: "km"
        }
    },
    weeklyStats: {
        stepsData: [8500, 9200, 7800, 10500, 6800, 7500, 8900],
        caloriesData: [2100, 2300, 1950, 2400, 1800, 1850, 2150],
        activeMinutesData: [60, 75, 45, 80, 30, 45, 65],
        labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    },
    activities: [
        {
            id: 1,
            type: "walk",
            title: "Morning Walk",
            duration: 30,
            calories: 150,
            steps: 3500,
            timestamp: "2025-06-26T06:30:00Z",
            intensity: "moderate"
        },
        {
            id: 2,
            type: "run",
            title: "Evening Jog",
            duration: 25,
            calories: 300,
            steps: 2800,
            timestamp: "2025-06-26T18:00:00Z",
            intensity: "high"
        },
        {
            id: 3,
            type: "yoga",
            title: "Yoga Session",
            duration: 45,
            calories: 120,
            steps: 0,
            timestamp: "2025-06-26T07:30:00Z",
            intensity: "low"
        }
    ],
    goals: {
        daily: {
            steps: 10000,
            calories: 2200,
            activeMinutes: 60,
            water: 8
        },
        weekly: {
            workouts: 5,
            totalSteps: 70000,
            totalCalories: 15400
        }
    },
    achievements: [
        {
            id: 1,
            title: "Step Master",
            description: "Reached 10,000 steps",
            icon: "steps",
            earned: true,
            date: "2025-06-25"
        },
        {
            id: 2,
            title: "Consistency King",
            description: "7 days workout streak",
            icon: "streak",
            earned: false,
            progress: 5
        }
    ]
}