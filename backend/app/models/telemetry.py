from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class Position(BaseModel):
    """GPS and normalized position data"""
    latitude: float = Field(..., ge=-90, le=90, description="Latitude in degrees")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude in degrees")
    altitude: Optional[float] = Field(None, description="Altitude in meters")
    normalized_x: Optional[float] = Field(None, description="Track X coordinate (0-1000)")
    normalized_y: Optional[float] = Field(None, description="Track Y coordinate (0-1000)")


class Motion(BaseModel):
    """Motion and acceleration data from IMU"""
    speed: Optional[float] = Field(None, description="Speed in km/h")
    acceleration_x: Optional[float] = Field(None, description="Lateral G-force")
    acceleration_y: Optional[float] = Field(None, description="Longitudinal G-force")
    acceleration_z: Optional[float] = Field(None, description="Vertical G-force")
    heading: Optional[float] = Field(None, ge=0, le=360, description="Compass heading")


class Sensors(BaseModel):
    """Additional sensor readings"""
    temperature_engine: Optional[float] = Field(None, description="Engine temp in Celsius")
    temperature_ambient: Optional[float] = Field(None, description="Ambient temp in Celsius")


class TelemetryData(BaseModel):
    """Complete telemetry packet"""
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    device_id: str = Field(..., min_length=1, description="Unique device identifier")
    position: Position
    motion: Optional[Motion] = None
    sensors: Optional[Sensors] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-02-25T10:30:00Z",
                "device_id": "esp32-car-01",
                "position": {
                    "latitude": 51.5074,
                    "longitude": -0.1278,
                    "altitude": 15.5,
                    "normalized_x": 450.2,
                    "normalized_y": 320.8
                },
                "motion": {
                    "speed": 245.5,
                    "acceleration_x": 1.2,
                    "acceleration_y": 0.8,
                    "acceleration_z": -0.1,
                    "heading": 87.3
                },
                "sensors": {
                    "temperature_engine": 95.2,
                    "temperature_ambient": 22.5
                }
            }
        }