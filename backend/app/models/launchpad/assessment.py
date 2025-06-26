from pydantic import BaseModel, ValidationError, root_validator
from typing import List, Dict, Any, Optional
from .hra import HraStep

class AssessmentTemplatePayload(BaseModel):
    template_id: str
    name: str
    description: Optional[str] = None
    steps: List[HraStep]

class AssessmentAnswersPayload(BaseModel):
    answers: Dict[str, Any]  # question_id -> answer value

    @root_validator(pre=True)
    def check_answers_not_empty(cls, values):
        answers = values.get('answers')
        if not answers or not isinstance(answers, dict):
            raise ValueError('Answers must be a non-empty dictionary')
        return values 