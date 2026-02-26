from typing import Tuple
from app.models.session import TrackSector


class SectorManager:
    """Determines which track sector a car is in based on normalized coordinates"""
    
    def __init__(self):
        # Red Bull Ring sector boundaries (normalized 0-1000 coordinates)
        # Sector 1: Start → Turn 3
        # Sector 2: Turn 3 → Turn 6
        # Sector 3: Turn 6 → Start/Finish
        
        self.sector_boundaries = {
            TrackSector.SECTOR_1: {
                "x_min": 0, "x_max": 400,
                "y_min": 0, "y_max": 1000
            },
            TrackSector.SECTOR_2: {
                "x_min": 400, "x_max": 700,
                "y_min": 0, "y_max": 1000
            },
            TrackSector.SECTOR_3: {
                "x_min": 700, "x_max": 1000,
                "y_min": 0, "y_max": 1000
            }
        }
    
    def get_sector(self, normalized_x: float, normalized_y: float) -> TrackSector:
        """Determine which sector a car is in"""
        for sector, bounds in self.sector_boundaries.items():
            if (bounds["x_min"] <= normalized_x <= bounds["x_max"] and
                bounds["y_min"] <= normalized_y <= bounds["y_max"]):
                return sector
        
        return TrackSector.SECTOR_1  # Default
    
    def is_in_sector(
        self, 
        normalized_x: float, 
        normalized_y: float, 
        sector: TrackSector
    ) -> bool:
        """Check if coordinates are in a specific sector"""
        current_sector = self.get_sector(normalized_x, normalized_y)
        return current_sector == sector


sector_manager = SectorManager()