"""
Generate simulated telemetry data for testing multi-car display
"""
import requests
import json
import time
import math
from datetime import datetime

API_URL = "http://localhost:8000/api/v1"

# Test cars with 2026 F1 teams
TEST_CARS = [
    {
        "device_id": "esp32-car-01",
        "car_number": 1,
        "driver_name": "Max Verstappen",
        "team": "red_bull"
    },
    {
        "device_id": "esp32-car-02",
        "car_number": 16,
        "driver_name": "Charles Leclerc",
        "team": "ferrari"
    },
    {
        "device_id": "esp32-car-03",
        "car_number": 63,
        "driver_name": "George Russell",
        "team": "mercedes"
    }
]

def fetch_track_layout():
    """Get Red Bull Ring waypoints from backend"""
    try:
        response = requests.get(f"{API_URL}/track/layout")
        if response.status_code == 200:
            data = response.json()
            return data["waypoints"]
    except Exception as e:
        print(f"[ERROR] Failed to fetch track layout: {e}")
    return None

def interpolate_position(waypoints, lap_progress):
    """Interpolate GPS position along track waypoints"""
    if not waypoints or len(waypoints) < 2:
        angle_rad = lap_progress * 2 * math.pi
        lat = 47.2197 + 0.01 * math.cos(angle_rad)
        lon = 14.7647 + 0.01 * math.sin(angle_rad)
        return lat, lon
    
    total_segments = len(waypoints) - 1
    segment_progress = lap_progress * total_segments
    segment_index = int(segment_progress)
    
    if segment_index >= total_segments:
        segment_index = total_segments - 1
        local_progress = 1.0
    else:
        local_progress = segment_progress - segment_index
    
    wp1 = waypoints[segment_index]
    wp2 = waypoints[(segment_index + 1) % len(waypoints)]
    
    lat = wp1["gps"]["latitude"] + (wp2["gps"]["latitude"] - wp1["gps"]["latitude"]) * local_progress
    lon = wp1["gps"]["longitude"] + (wp2["gps"]["longitude"] - wp1["gps"]["longitude"]) * local_progress
    
    return lat, lon

def calculate_heading(waypoints, lap_progress):
    """Calculate heading based on track direction"""
    if not waypoints or len(waypoints) < 2:
        return (lap_progress * 360) % 360
    
    total_segments = len(waypoints) - 1
    segment_progress = lap_progress * total_segments
    segment_index = int(segment_progress) % total_segments
    
    wp1 = waypoints[segment_index]
    wp2 = waypoints[(segment_index + 1) % len(waypoints)]
    
    lat1 = math.radians(wp1["gps"]["latitude"])
    lon1 = math.radians(wp1["gps"]["longitude"])
    lat2 = math.radians(wp2["gps"]["latitude"])
    lon2 = math.radians(wp2["gps"]["longitude"])
    
    dLon = lon2 - lon1
    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dLon)
    bearing = math.atan2(y, x)
    
    return (math.degrees(bearing) + 360) % 360

def generate_telemetry(car, lap_progress, waypoints, speed_factor=1.0):
    """Generate realistic telemetry for a car following actual track layout"""
    
    # Get position from track waypoints
    lat, lon = interpolate_position(waypoints, lap_progress)
    
    # Simulate speed variations (slower in corners)
    corner_slowdown = abs(math.sin(lap_progress * 12 * math.pi)) * 0.4  # More corner variation
    base_speed = 250 * speed_factor
    speed = base_speed * (1 - corner_slowdown)
    
    # Simulate G-forces
    acceleration_x = math.sin(lap_progress * 10 * math.pi) * 2.8
    acceleration_y = math.cos(lap_progress * 8 * math.pi) * 2.2
    
    # Get realistic heading from track direction
    heading = calculate_heading(waypoints, lap_progress)
    
    # Engine temperature varies with speed
    engine_temp = 85 + (speed / 250) * 15
    
    return {
        "device_id": car["device_id"],
        "position": {
            "latitude": lat,
            "longitude": lon,
            "altitude": 678.0
        },
        "motion": {
            "speed": speed,
            "acceleration_x": acceleration_x,
            "acceleration_y": acceleration_y,
            "acceleration_z": -0.2,
            "heading": heading
        },
        "sensors": {
            "temperature_engine": engine_temp,
            "temperature_ambient": 22.5
        }
    }

def start_session():
    """Initialize race session"""
    print("=" * 60)
    print("MULTI-CAR SIMULATION TEST")
    print("=" * 60)
    
    # Start session
    print("\n[1/3] Starting session...")
    response = requests.post(f"{API_URL}/session/start?session_id=test-multicar&session_type=race")
    print(f"Status: {response.status_code}")
    
    # Register cars
    print("\n[2/3] Registering cars...")
    for car in TEST_CARS:
        response = requests.get(f"{API_URL}/cars/teams")
        teams = response.json()["teams"]
        
        car_data = {
            **car,
            "team_colors": teams[car["team"]]
        }
        
        response = requests.post(f"{API_URL}/cars/register", json=car_data)
        if response.status_code == 200:
            print(f"  Registered: {car['driver_name']} (#{car['car_number']}) - {teams[car['team']]['name']}")
    
    print("\n[3/3] Starting telemetry stream...\n")

def run_simulation(duration_seconds=60, waypoints=None):
    """Run multi-car simulation following track layout"""
    start_time = time.time()
    lap_progress = [0.0, 0.15, 0.3]  # Stagger car positions
    
    iteration = 0
    
    while time.time() - start_time < duration_seconds:
        iteration += 1
        
        for i, car in enumerate(TEST_CARS):
            speed_multiplier = 1.0 + (i * 0.05)
            lap_progress[i] = (lap_progress[i] + 0.005 * speed_multiplier) % 1.0
            
            # Generate telemetry with waypoints
            telemetry = generate_telemetry(car, lap_progress[i], waypoints, speed_multiplier)
            
            try:
                response = requests.post(f"{API_URL}/telemetry", json=telemetry)
                if response.status_code == 200:
                    sector = int(lap_progress[i] * 3) + 1
                    print(f"[T+{iteration:03d}] {car['driver_name']}: {telemetry['motion']['speed']:.1f} km/h | Sector {sector}")
            except Exception as e:
                print(f"Error sending telemetry: {e}")
        
        print()
        time.sleep(0.5)

def trigger_flag_scenario():
    """Trigger a flag scenario during simulation"""
    print("\n" + "=" * 60)
    print("TRIGGERING FLAG SCENARIO")
    print("=" * 60 + "\n")
    
    scenarios = [
        {
            "delay": 5,
            "flag_type": "yellow",
            "full_course": False,
            "sectors": ["sector_2"],
            "message": "Debris at Turn 4"
        },
        {
            "delay": 10,
            "flag_type": "green",
            "full_course": True,
            "message": "Track clear - racing resumed"
        }
    ]
    
    for scenario in scenarios:
        time.sleep(scenario["delay"])
        print(f"Setting {scenario['flag_type'].upper()} flag...")
        requests.post(f"{API_URL}/flags/set", json={
            "flag_type": scenario["flag_type"],
            "full_course": scenario["full_course"],
            "sectors": scenario.get("sectors", []),
            "message": scenario["message"]
        })

if __name__ == "__main__":
    import threading
    
    try:
        start_session()
        
        # Fetch track layout
        print("\n[TRACK] Fetching Red Bull Ring layout...")
        waypoints = fetch_track_layout()
        
        if waypoints:
            print(f"[SUCCESS] Track layout loaded with {len(waypoints)} waypoints\n")
        else:
            print("[WARNING] Using fallback circular pattern\n")
        
        # Start flag scenario in background
        flag_thread = threading.Thread(target=trigger_flag_scenario, daemon=True)
        flag_thread.start()
        
        # Run simulation with track layout
        run_simulation(duration_seconds=30, waypoints=waypoints)
        
        print("\n" + "=" * 60)
        print("SIMULATION COMPLETE")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
    except Exception as e:
        print(f"\nError: {e}")