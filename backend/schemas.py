from pydantic import BaseModel
from typing import Optional


class SkillCreate(BaseModel):
    name: str
    category: Optional[str] = None

class PracticeEventCreate(BaseModel):
    skill_id: str
    source: str = "manual"
    intensity: float = 1.0