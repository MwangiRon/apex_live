from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime

from app.models import TelemetryData
from app.logic.coordinate_normalizer import CoordinateNormalizer, redbull_ring_normalizer

router = APIRouter(prefix="/api/v1", tags=["telemetry"])

# In-memory storage (replace with database later)
telemetry_store: List[TelemetryData] = []


@router.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "F1 Telemetry API",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat(),
        "track": "Red Bull Ring, Spielberg, Austria"
    }


@router.post("/telemetry", response_model=TelemetryData)
async def receive_telemetry(data: TelemetryData):
    """
    Receive telemetry data from ESP32 devices.
    Auto-normalizes coordinates using Red Bull Ring reference.
    """
    # If normalized coordinates not provided, calculate them
    if data.position.normalized_x is None or data.position.normalized_y is None:
        norm_x, norm_y = redbull_ring_normalizer.normalize(
            data.position.latitude,
            data.position.longitude
        )
        data.position.normalized_x = norm_x
        data.position.normalized_y = norm_y
    
    # Store in memory (later: save to database)
    telemetry_store.append(data)
    
    # Keep only last 1000 records to prevent memory issues
    if len(telemetry_store) > 1000:
        telemetry_store.pop(0)
    
    return data


@router.get("/telemetry/latest", response_model=List[TelemetryData])
async def get_latest_telemetry(limit: int = 10, device_id: str = None):
    """
    Get latest telemetry records.
    
    Args:
        limit: Number of records to return (default 10, max 100)
        device_id: Optional filter by device ID
    """
    limit = min(limit, 100)  # Cap at 100
    
    # Filter by device if specified
    if device_id:
        filtered = [t for t in telemetry_store if t.device_id == device_id]
        return filtered[-limit:]
    
    return telemetry_store[-limit:]


@router.get("/track/info")
async def get_track_info():
    """Get information about the current track configuration"""
    return {
        "name": "Red Bull Ring",
        "location": "Spielberg, Austria",
        "length_km": 4.318,
        "turns": 10,
        "center": {
            "latitude": redbull_ring_normalizer.center_lat,
            "longitude": redbull_ring_normalizer.center_lon
        },
        "dimensions": {
            "width_meters": redbull_ring_normalizer.width,
            "height_meters": redbull_ring_normalizer.height
        },
        "notable_corners": [
            {"turn": 1, "name": "Castrol Edge"},
            {"turn": 3, "name": "Remus"},
            {"turn": 4, "name": "Schlossgold"},
            {"turn": 7, "name": "Rindt"},
            {"turn": 9, "name": "Jochen Rindt Kurve"}
        ]
    }


@router.delete("/telemetry/clear")
async def clear_telemetry():
    """Clear all stored telemetry data (dev/test only)"""
    telemetry_store.clear()
    return {"message": "Telemetry data cleared", "count": 0}