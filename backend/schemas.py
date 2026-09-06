from pydantic import BaseModel
from typing import Optional


class SkillCreate(BaseModel):
    name: str
    category: Optional[str] = None