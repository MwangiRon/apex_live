from typing import Tuple, List
import math


class TrackWaypoint:
    """Single GPS waypoint on the track"""
    def __init__(self, lat: float, lon: float, name: str = ""):
        self.lat = lat
        self.lon = lon
        self.name = name


class CoordinateNormalizer:
    """
    Converts GPS coordinates to normalized track coordinates (0-1000 range).
    Now supports track-specific waypoints for realistic layout.
    """
    
    def __init__(
        self,
        track_center_lat: float,
        track_center_lon: float,
        track_width_meters: float = 1000.0,
        track_height_meters: float = 1000.0,
        waypoints: List[TrackWaypoint] = None
    ):
        self.center_lat = track_center_lat
        self.center_lon = track_center_lon
        self.width = track_width_meters
        self.height = track_height_meters
        self.waypoints = waypoints or []
        
        self.meters_per_degree_lat = 111320.0
        
    def normalize(self, latitude: float, longitude: float) -> Tuple[float, float]:
        """Convert GPS coordinates to normalized track coordinates"""
        lat_offset_meters = (latitude - self.center_lat) * self.meters_per_degree_lat
        
        meters_per_degree_lon = self.meters_per_degree_lat * math.cos(math.radians(self.center_lat))
        lon_offset_meters = (longitude - self.center_lon) * meters_per_degree_lon
        
        normalized_x = 500 + (lon_offset_meters / self.width) * 1000
        normalized_y = 500 + (lat_offset_meters / self.height) * 1000
        
        normalized_x = max(0, min(1000, normalized_x))
        normalized_y = max(0, min(1000, normalized_y))
        
        return normalized_x, normalized_y


# Red Bull Ring actual GPS waypoints
RED_BULL_RING_WAYPOINTS = [
    TrackWaypoint(47.2197, 14.7620, "Start/Finish"),
    TrackWaypoint(47.2207, 14.7625, "Turn 1 - Castrol Edge"),
    TrackWaypoint(47.2215, 14.7635, "Turn 2"),
    TrackWaypoint(47.2220, 14.7650, "Turn 3 - Remus"),
    TrackWaypoint(47.2218, 14.7668, "Turn 4 - Schlossgold"),
    TrackWaypoint(47.2205, 14.7680, "Turn 5"),
    TrackWaypoint(47.2190, 14.7685, "Turn 6 - Rauch"),
    TrackWaypoint(47.2175, 14.7675, "Turn 7 - Rindt"),
    TrackWaypoint(47.2170, 14.7655, "Turn 8"),
    TrackWaypoint(47.2180, 14.7635, "Turn 9 - Jochen Rindt"),
    TrackWaypoint(47.2190, 14.7625, "Turn 10"),
    TrackWaypoint(47.2197, 14.7620, "Back to Start/Finish"),
]

redbull_ring_normalizer = CoordinateNormalizer(
    track_center_lat=47.2197,
    track_center_lon=14.7647,
    track_width_meters=1500.0,
    track_height_meters=2000.0,
    waypoints=RED_BULL_RING_WAYPOINTS
)