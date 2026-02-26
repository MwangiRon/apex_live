from pydantic import BaseModel, Field
from typing import Optional


class TeamColor(BaseModel):
    """F1 Team color scheme"""
    primary: str = Field(..., description="Primary hex color (e.g., #FF1E23)")
    secondary: str = Field(..., description="Secondary hex color")
    name: str = Field(..., description="Team name")


class Car(BaseModel):
    """Individual car/driver configuration"""
    device_id: str = Field(..., description="ESP32 device identifier")
    car_number: int = Field(..., ge=1, le=99, description="Race number")
    driver_name: str = Field(..., description="Driver name")
    team: str = Field(..., description="Team identifier (e.g., 'red_bull')")
    team_colors: TeamColor
    
    class Config:
        json_schema_extra = {
            "example": {
                "device_id": "esp32-car-01",
                "car_number": 1,
                "driver_name": "Max Verstappen",
                "team": "red_bull",
                "team_colors": {
                    "primary": "#1E41FF",
                    "secondary": "#FCD700",
                    "name": "Red Bull Racing"
                }
            }
        }


# F1 2026 Team Color Palette
F1_TEAMS_2026 = {
    "red_bull": TeamColor(primary="#1E41FF", secondary="#FFFFFF", name="Oracle Red Bull Racing"),
    "ferrari": TeamColor(primary="#FF2800", secondary="#FFFFFF", name="Scuderia Ferrari HP"),
    "mercedes": TeamColor(primary="#C0C0C0", secondary="#00A19B", name="Mercedes-AMG PETRONAS F1 Team"),
    "mclaren": TeamColor(primary="#FF8700", secondary="#000000", name="McLaren Mastercard F1 Team"),
    "aston_martin": TeamColor(primary="#006F62", secondary="#FDE100", name="Aston Martin Aramco F1 Team"),
    "alpine": TeamColor(primary="#0090FF", secondary="#FF5F9E", name="BWT Alpine F1 Team"),
    "williams": TeamColor(primary="#005AFF", secondary="#FFFFFF", name="Atlassian Williams F1 Team"),
    "racing_bulls": TeamColor(primary="#FFFFFF", secondary="#2B6EB2", name="Visa Cash App Racing Bulls F1 Team"),
    "audi": TeamColor(primary="#C0C0C0", secondary="#D10000", name="Audi Revolut F1 Team"),
    "haas": TeamColor(primary="#FFFFFF", secondary="#E60000", name="TGR Haas F1 Team"),
    "cadillac": TeamColor(primary="#000000", secondary="#FFFFFF", name="Cadillac F1 Team"),
}