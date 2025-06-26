from pydantic import BaseModel
from typing import List

class Benefit(BaseModel):
    id: int
    title: str
    description: str
    icon: str

class Feature(BaseModel):
    id: int
    title: str
    description: str
    image: str

class Testimonial(BaseModel):
    id: int
    name: str
    role: str
    quote: str
    rating: int
    image: str

class CtaButton(BaseModel):
    id: int
    text: str
    type: str
    action: str
    target: str

class Wellness(BaseModel):
    welcomeMessage: str
    subtitle: str
    benefits: List[Benefit]
    features: List[Feature]
    testimonials: List[Testimonial]
    ctaButtons: List[CtaButton] 