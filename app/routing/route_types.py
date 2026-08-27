from enum import Enum
from pydantic import BaseModel
from typing import List

class RouteDestination(str, Enum):
    LOCAL = "local"
    EXTERNAL = "external"

class RoutingDecision(BaseModel):
    route: RouteDestination
    reason: str
    confidence: float
    allowed_tools: List[str]