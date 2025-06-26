from pydantic import BaseModel
from typing import List, Dict, Any, Optional

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
    placeholder: Optional[str] = None
    validation: Optional[Dict[str, Any]] = None

class ProfileStep(BaseModel):
    step: int
    questions: List[Question]
    userResponses: Dict[str, Any]
    validationErrors: Dict[str, Any] 