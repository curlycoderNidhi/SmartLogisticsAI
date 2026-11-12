from pydantic import BaseModel
from datetime import datetime

class ShipmentCreate(BaseModel):
    tracking_number: str
    origin: str
    destination: str
    distance_km: float
    weather_condition: str
    status: str = "In-Transit"

class ShipmentResponse(ShipmentCreate):
    id: int
    ai_risk_score: float
    ai_recommendation: str
    created_at: datetime

    class Config:
        from_attributes = True