export const basicProfileMockData = {
    step1: {
        step: 1,
        questions: [
            {
                id: "age",
                type: "number",
                label: "What's your age?",
                placeholder: "Enter your age",
                required: true,
                validation: { min: 13, max: 120 }
            },
            {
                id: "gender",
                type: "radio",
                label: "Select your gender",
                required: true,
                options: [
                    { value: "male", label: "Male", icon: "male" },
                    { value: "female", label: "Female", icon: "female" },
                    { value: "other", label: "Others", icon: "other" }
                ]
            }
        ],
        userResponses: {},
        validationErrors: {}
    },
    step2: {
        step: 2,
        questions: [
            {
                id: "height",
                type: "number",
                label: "What's your height?",
                placeholder: "Enter height in cm",
                required: true,
                validation: { min: 50, max: 250 }
            },
            {
                id: "weight",
                type: "number",
                label: "What's your current weight?",
                placeholder: "Enter weight in kg",
                required: true,
                validation: { min: 20, max: 300 }
            }
        ],
        userResponses: {},
        validationErrors: {}
    },
    step3: {
        step: 3,
        questions: [
            {
                id: "medicalConditions",
                type: "checkbox",
                label: "Do you have any of these medical conditions?",
                required: false,
                options: [
                    { value: "diabetes", label: "Diabetes" },
                    { value: "hypertension", label: "High Blood Pressure" },
                    { value: "heart_disease", label: "Heart Disease" },
                    { value: "asthma", label: "Asthma" },
                    { value: "none", label: "None of the above" }
                ]
            },
            {
                id: "medications",
                type: "textarea",
                label: "Are you currently taking any medications?",
                placeholder: "List your current medications (optional)",
                required: false
            }
        ],
        userResponses: {},
        validationErrors: {}
    }
}