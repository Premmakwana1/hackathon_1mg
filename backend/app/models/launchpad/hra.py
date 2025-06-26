from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class Option(BaseModel):
    value: str
    label: str
    icon: Optional[str] = None

class Question(BaseModel):
    id: str
    type: str
    label: str
    required: bool
    options: Optional[List[Option]] = None
    min: Optional[int] = None
    max: Optional[int] = None
    labels: Optional[Dict[str, str]] = None
    placeholder: Optional[str] = None
    validation: Optional[Dict[str, Any]] = None

class RiskFactor(BaseModel):
    category: str
    risk: str
    factors: List[str]

class HraStep(BaseModel):
    step: int
    questions: List[Question]
    responses: Dict[str, Any]
    riskFactors: List[RiskFactor]
    recommendations: List[str] 