export const searchMockData = {
    query: "",
    results: [
        {
            id: 1,
            type: "exercise",
            title: "Push-ups",
            description: "Chest and arm strengthening exercise",
            category: "Strength Training",
            difficulty: "Beginner",
            duration: "10-15 minutes",
            image: "/images/pushups.jpg"
        },
        {
            id: 2,
            type: "exercise",
            title: "Morning Yoga",
            description: "Gentle yoga routine for flexibility",
            category: "Flexibility",
            difficulty: "Beginner",
            duration: "20-30 minutes",
            image: "/images/yoga.jpg"
        },
        {
            id: 3,
            type: "recipe",
            title: "Protein Smoothie",
            description: "High-protein breakfast smoothie",
            category: "Nutrition",
            difficulty: "Easy",
            duration: "5 minutes",
            image: "/images/smoothie.jpg"
        },
        {
            id: 4,
            type: "article",
            title: "Benefits of Walking",
            description: "Health benefits of daily walking",
            category: "Health Tips",
            readTime: "3 minutes",
            image: "/images/walking.jpg"
        }
    ],
    filters: {
        categories: ["All", "Exercise", "Nutrition", "Health Tips", "Mental Health"],
        difficulty: ["All", "Beginner", "Intermediate", "Advanced"],
        duration: ["All", "Under 10 min", "10-30 min", "30+ min"]
    },
    suggestions: [
        "Weight loss exercises",
        "Healthy breakfast recipes",
        "Stress management techniques",
        "Heart-healthy foods",
        "Sleep improvement tips"
    ],
    popularSearches: [
        "cardio workout",
        "meditation",
        "protein recipes",
        "yoga for beginners",
        "healthy snacks"
    ]
}