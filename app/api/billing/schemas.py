# Optional: For Flutter type hints
from pydantic import BaseModel
from typing import List, Any

class PlanOut(BaseModel):
    plan: str
    monthly: float
    yearly: float
    trial_days: int
    features: List[Any]
