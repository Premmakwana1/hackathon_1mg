from pydantic import BaseModel, Field
from typing import List, Dict, Any

class Widget(BaseModel):
    widget_id: int
    widget_name: str
    value: Any

class Form(BaseModel):
    tabs: List[str]
    widgets: Dict[str, List[Widget]]

class User(BaseModel):
    id: int
    name: str
    form: Form 