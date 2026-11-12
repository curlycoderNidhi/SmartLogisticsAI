from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base

class Shipment(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True)
    origin = Column(String)
    destination = Column(String)
    distance_km = Column(Float)
    weather_condition = Column(String)  # Clear, Rain, Storm, Fog
    status = Column(String, default="In-Transit")
    ai_risk_score = Column(Float)
    ai_recommendation = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)