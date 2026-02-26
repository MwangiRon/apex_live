from typing import Tuple
import math


class CoordinateNormalizer:
    """
    Converts GPS coordinates to normalized track coordinates (0-1000 range).
    This same logic should be mirrored in frontend and ESP32.
    """
    
    def __init__(
        self,
        track_center_lat: float,
        track_center_lon: float,
        track_width_meters: float = 1000.0,
        track_height_meters: float = 1000.0
    ):
        """
        Args:
            track_center_lat: Track center latitude
            track_center_lon: Track center longitude
            track_width_meters: Track width in meters (default 1km)
            track_height_meters: Track height in meters (default 1km)
        """
        self.center_lat = track_center_lat
        self.center_lon = track_center_lon
        self.width = track_width_meters
        self.height = track_height_meters
        
        # Approximate conversion: 1 degree latitude ≈ 111,320 meters
        self.meters_per_degree_lat = 111320.0
        
    def normalize(self, latitude: float, longitude: float) -> Tuple[float, float]:
        """
        Convert GPS coordinates to normalized track coordinates.
        
        Args:
            latitude: GPS latitude
            longitude: GPS longitude
            
        Returns:
            Tuple of (normalized_x, normalized_y) in range 0-1000
        """
        # Calculate offset from track center in meters
        lat_offset_meters = (latitude - self.center_lat) * self.meters_per_degree_lat
        
        # Longitude conversion depends on latitude (cos correction)
        meters_per_degree_lon = self.meters_per_degree_lat * math.cos(math.radians(self.center_lat))
        lon_offset_meters = (longitude - self.center_lon) * meters_per_degree_lon
        
        # Normalize to 0-1000 range
        normalized_x = 500 + (lon_offset_meters / self.width) * 1000
        normalized_y = 500 + (lat_offset_meters / self.height) * 1000
        
        # Clamp to valid range
        normalized_x = max(0, min(1000, normalized_x))
        normalized_y = max(0, min(1000, normalized_y))
        
        return normalized_x, normalized_y


# Red Bull Ring (Spielberg, Austria)
# Track length: 4.318 km
# Track center coordinates (approximate middle of the circuit)
redbull_ring_normalizer = CoordinateNormalizer(
    track_center_lat=47.2197,  # Red Bull Ring center latitude
    track_center_lon=14.7647,  # Red Bull Ring center longitude
    track_width_meters=1500.0,  # Track spans ~1.5km east-west
    track_height_meters=2000.0  # Track spans ~2km north-south
)

# You can add more tracks here in the future
# Example: Monaco, Monza, Spa, etc.