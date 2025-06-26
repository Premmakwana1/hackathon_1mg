from pydantic import BaseModel
from typing import List, Optional

class Stat(BaseModel):
    current: float
    goal: float
    progress: int
    unit: str

class TodayStats(BaseModel):
    steps: Stat
    calories: Stat
    activeMinutes: Stat
    distance: Stat

class WeeklyStats(BaseModel):
    stepsData: List[int]
    caloriesData: List[int]
    activeMinutesData: List[int]
    labels: List[str]

class Activity(BaseModel):
    id: int
    type: str
    title: str
    duration: int
    calories: int
    steps: int
    timestamp: str
    intensity: str

class DailyGoals(BaseModel):
    steps: int
    calories: int
    activeMinutes: int
    water: int

class WeeklyGoals(BaseModel):
    workouts: int
    totalSteps: int
    totalCalories: int

class Goals(BaseModel):
    daily: DailyGoals
    weekly: WeeklyGoals

class Achievement(BaseModel):
    id: int
    title: str
    description: str
    icon: str
    earned: bool
    date: Optional[str] = None
    progress: Optional[int] = None

class ActivityTracker(BaseModel):
    todayStats: TodayStats
    weeklyStats: WeeklyStats
    activities: List[Activity]
    goals: Goals
    achievements: List[Achievement] 