from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum
from datetime import datetime


class FlagType(str, Enum):
    """Race control flag types"""
    GREEN = "green"           # Racing
    YELLOW = "yellow"         # Caution (sector-specific or full course)
    DOUBLE_YELLOW = "double_yellow"  # No overtaking
    RED = "red"               # Session stopped
    BLUE = "blue"             # Lapped car
    BLACK = "black"           # Disqualification
    CHEQUERED = "chequered"   # Race end


class TrackSector(str, Enum):
    """Track sector identifiers"""
    SECTOR_1 = "sector_1"
    SECTOR_2 = "sector_2"
    SECTOR_3 = "sector_3"


class FlagState(BaseModel):
    """Current flag state"""
    flag_type: FlagType
    full_course: bool = Field(default=False, description="Full course flag vs sector-specific")
    affected_sectors: List[TrackSector] = Field(default_factory=list)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    message: Optional[str] = None


class SessionState(BaseModel):
    """Complete race session state"""
    session_id: str
    session_type: str = Field(default="race", description="practice/qualifying/race")
    active_cars: List[str] = Field(default_factory=list, description="List of device_ids")
    current_flag: FlagState = Field(
        default_factory=lambda: FlagState(flag_type=FlagType.GREEN, full_course=True)
    )
    lap_count: int = Field(default=0)
    session_time_remaining: Optional[int] = Field(None, description="Seconds remaining")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "redbull-ring-race-2024",
                "session_type": "race",
                "active_cars": ["esp32-car-01", "esp32-car-02"],
                "current_flag": {
                    "flag_type": "yellow",
                    "full_course": False,
                    "affected_sectors": ["sector_2"],
                    "timestamp": "2024-02-26T10:30:00Z",
                    "message": "Incident at Turn 4"
                },
                "lap_count": 15,
                "session_time_remaining": 3600
            }
        }