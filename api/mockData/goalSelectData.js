export const goalSelectMockData = {
    step1: {
        step: 1,
        availableGoals: [
            {
                id: "weight_loss",
                title: "Weight Loss",
                description: "Lose weight in a healthy and sustainable way",
                icon: "weight-loss",
                difficulty: "Medium",
                duration: "3-6 months",
                benefits: ["Improved energy", "Better sleep", "Reduced health risks"]
            },
            {
                id: "muscle_gain",
                title: "Muscle Building",
                description: "Build lean muscle and increase strength",
                icon: "muscle",
                difficulty: "High",
                duration: "6-12 months",
                benefits: ["Increased strength", "Better metabolism", "Improved posture"]
            },
            {
                id: "cardio_fitness",
                title: "Cardiovascular Fitness",
                description: "Improve heart health and endurance",
                icon: "heart",
                difficulty: "Medium",
                duration: "2-4 months",
                benefits: ["Better stamina", "Heart health", "Increased energy"]
            },
            {
                id: "flexibility",
                title: "Flexibility & Mobility",
                description: "Improve flexibility and reduce stiffness",
                icon: "yoga",
                difficulty: "Low",
                duration: "1-3 months",
                benefits: ["Reduced pain", "Better posture", "Injury prevention"]
            }
        ],
        selectedGoals: [],
        recommendations: []
    },
    step2: {
        step: 2,
        availableGoals: [
            {
                id: "stress_management",
                title: "Stress Management",
                description: "Learn techniques to manage daily stress",
                icon: "meditation",
                difficulty: "Low",
                duration: "1-2 months",
                benefits: ["Better mood", "Improved sleep", "Reduced anxiety"]
            },
            {
                id: "better_sleep",
                title: "Better Sleep",
                description: "Improve sleep quality and duration",
                icon: "sleep",
                difficulty: "Medium",
                duration: "1-3 months",
                benefits: ["More energy", "Better focus", "Improved mood"]
            },
            {
                id: "nutrition",
                title: "Healthy Nutrition",
                description: "Develop healthy eating habits",
                icon: "nutrition",
                difficulty: "Medium",
                duration: "2-6 months",
                benefits: ["Better energy", "Weight management", "Overall health"]
            },
            {
                id: "hydration",
                title: "Proper Hydration",
                description: "Maintain optimal hydration levels",
                icon: "water",
                difficulty: "Low",
                duration: "2-4 weeks",
                benefits: ["Better skin", "Improved energy", "Better digestion"]
            }
        ],
        selectedGoals: [],
        recommendations: [
            "Based on your profile, we recommend starting with 2-3 goals",
            "Focus on lifestyle goals alongside fitness goals for better results"
        ]
    }
}