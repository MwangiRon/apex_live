from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from app.models.car import Car, F1_TEAMS_2026 as F1_TEAMS
from app.models.session import SessionState, FlagType, FlagState, TrackSector
from app.logic.race_controller import race_controller
from app.logic.sector_manager import sector_manager
from app.transport.websocket_handler import manager

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
    
    # Broadcast telemetry to all connected WebSocket clients
    await manager.broadcast_telemetry(data.dict())
    
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

@router.get("/track/layout")
async def get_track_layout():
    """Get track waypoints for visualization"""
    from app.logic.coordinate_normalizer import RED_BULL_RING_WAYPOINTS, redbull_ring_normalizer
    
    waypoints_normalized = []
    for waypoint in RED_BULL_RING_WAYPOINTS:
        norm_x, norm_y = redbull_ring_normalizer.normalize(
            waypoint.lat,
            waypoint.lon
        )
        waypoints_normalized.append({
            "name": waypoint.name,
            "gps": {
                "latitude": waypoint.lat,
                "longitude": waypoint.lon
            },
            "normalized": {
                "x": norm_x,
                "y": norm_y
            }
        })
    
    return {
        "track_name": "Red Bull Ring",
        "waypoints": waypoints_normalized,
        "total_corners": 10
    }
    
# ============= CAR REGISTRATION =============

@router.post("/cars/register", response_model=Car)
async def register_car(car: Car):
    """
    Register a new car in the session.
    This associates a device_id with driver info and team colors.
    """
    # Validate team exists
    if car.team not in F1_TEAMS:
        raise HTTPException(status_code=400, detail=f"Unknown team: {car.team}")
    
    # Auto-populate team colors if not provided
    if not car.team_colors:
        car.team_colors = F1_TEAMS[car.team]
    
    # Register with race controller
    race_controller.register_car(car.device_id)
    
    # Store car info (in-memory for now)
    # TODO: Add to database in future
    
    return car


@router.get("/cars/teams")
async def get_available_teams():
    """Get list of F1 teams with their colors"""
    return {
        "teams": {
            team_id: {
                "name": colors.name,
                "primary": colors.primary,
                "secondary": colors.secondary
            }
            for team_id, colors in F1_TEAMS.items()
        }
    }


# ============= SESSION MANAGEMENT =============

@router.post("/session/start")
async def start_session(session_id: str, session_type: str = "race"):
    """
    Start a new race session.
    This initializes the race controller with GREEN flag.
    """
    session = race_controller.create_session(session_id, session_type)
    return {
        "message": "Session started",
        "session": session
    }


@router.get("/session/status", response_model=SessionState)
async def get_session_status():
    """Get current session state including flag status"""
    session = race_controller.get_active_session()
    if not session:
        raise HTTPException(status_code=404, detail="No active session")
    return session


# ============= CAR REGISTRATION =============

@router.post("/cars/register", response_model=Car)
async def register_car(car: Car):
    """
    Register a new car in the session.
    This associates a device_id with driver info and team colors.
    """
    # Validate team exists
    if car.team not in F1_TEAMS:
        raise HTTPException(status_code=400, detail=f"Unknown team: {car.team}")
    
    # Auto-populate team colors if not provided
    if not car.team_colors:
        car.team_colors = F1_TEAMS[car.team]
    
    # Register with race controller
    race_controller.register_car(car.device_id)
    
    # Store car info (in-memory for now)
    # TODO: Add to database in future
    
    return car


@router.get("/cars/teams")
async def get_available_teams():
    """Get list of F1 teams with their colors"""
    return {
        "teams": {
            team_id: {
                "name": colors.name,
                "primary": colors.primary,
                "secondary": colors.secondary
            }
            for team_id, colors in F1_TEAMS.items()
        }
    }


# ============= SESSION MANAGEMENT =============

@router.post("/session/start")
async def start_session(session_id: str, session_type: str = "race"):
    """
    Start a new race session.
    This initializes the race controller with GREEN flag.
    """
    session = race_controller.create_session(session_id, session_type)
    return {
        "message": "Session started",
        "session": session
    }


@router.get("/session/status", response_model=SessionState)
async def get_session_status():
    """Get current session state including flag status"""
    session = race_controller.get_active_session()
    if not session:
        raise HTTPException(status_code=404, detail="No active session")
    return session


# ============= FLAG CONTROL =============

from pydantic import BaseModel

class FlagUpdate(BaseModel):
    flag_type: FlagType
    full_course: bool = True
    sectors: list[TrackSector] = None
    message: str = None

@router.post("/flags/set")
async def set_flag(flag_update: FlagUpdate):
    """
    Change the current flag state.
    
    Examples:
    - Green flag: {"flag_type": "green", "full_course": true}
    - Yellow in sector 2: {"flag_type": "yellow", "full_course": false, "sectors": ["sector_2"], "message": "Incident at Turn 4"}
    - Red flag: {"flag_type": "red", "full_course": true, "message": "Session stopped"}
    """
    try:
        flag_state = race_controller.set_flag(
            flag_type=flag_update.flag_type,
            full_course=flag_update.full_course,
            sectors=flag_update.sectors or [],
            message=flag_update.message
        )
        
        # Broadcast flag change to all connected clients
        await manager.broadcast_flag_change(flag_state.dict())
        
        return {
            "message": f"{flag_update.flag_type.value.upper()} flag set",
            "flag_state": flag_state
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/flags/current")
async def get_current_flag():
    """Get the current flag status"""
    flag_state = race_controller.get_flag_status()
    if not flag_state:
        raise HTTPException(status_code=404, detail="No active session")
    return flag_state
    
@router.delete("/telemetry/clear")
async def clear_telemetry():
    """Clear all stored telemetry data (dev/test only)"""
    telemetry_store.clear()
    return {"message": "Telemetry data cleared", "count": 0}