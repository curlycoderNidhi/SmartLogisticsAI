from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas, database, ai_service

# Create Database Tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="PulseHub AI Logistics Tracker")

# Serve static HTML files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_dashboard():
    return FileResponse("static/index.html")

@app.post("/api/shipments", response_model=schemas.ShipmentResponse)
def create_shipment(shipment: schemas.ShipmentCreate, db: Session = Depends(database.get_db)):
    # Check duplicate tracking number
    existing = db.query(models.Shipment).filter(models.Shipment.tracking_number == shipment.tracking_number).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tracking number already exists")

    # Run AI Risk Analysis
    risk_score, recommendation = ai_service.LogisticsAIService.analyze_shipment(
        shipment.distance_km, shipment.weather_condition, shipment.status
    )

    db_shipment = models.Shipment(
        **shipment.model_dump(),
        ai_risk_score=risk_score,
        ai_recommendation=recommendation
    )
    db.add(db_shipment)
    db.commit()
    db.refresh(db_shipment)
    return db_shipment

@app.get("/api/shipments", response_model=List[schemas.ShipmentResponse])
def get_all_shipments(db: Session = Depends(database.get_db)):
    return db.query(models.Shipment).order_by(models.Shipment.id.desc()).all()

@app.delete("/api/shipments/{shipment_id}")
def delete_shipment(shipment_id: int, db: Session = Depends(database.get_db)):
    shipment = db.query(models.Shipment).filter(models.Shipment.id == shipment_id).first()
    if not shipment:
        raise HTTPException(status_code=404, detail="Shipment not found")
    db.delete(shipment)
    db.commit()
    return {"message": "Shipment deleted successfully"}