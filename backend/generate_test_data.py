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

# Red Bull Ring track simulation
TRACK_CENTER_LAT = 47.2197
TRACK_CENTER_LON = 14.7647
TRACK_RADIUS = 0.01  # Approximate track radius in degrees

def generate_track_position(angle_degrees, offset_radius=0):
    """Generate GPS coordinates around Red Bull Ring circuit"""
    angle_rad = math.radians(angle_degrees)
    radius = TRACK_RADIUS + offset_radius
    
    lat = TRACK_CENTER_LAT + radius * math.cos(angle_rad)
    lon = TRACK_CENTER_LON + radius * math.sin(angle_rad)
    
    return lat, lon

def generate_telemetry(car, lap_progress, speed_factor=1.0):
    """Generate realistic telemetry for a car at a given lap progress"""
    
    # Calculate position on track (0-360 degrees)
    angle = lap_progress * 360
    
    # Add small offset per car to simulate racing line differences
    car_offset = (car["car_number"] % 3) * 0.001
    lat, lon = generate_track_position(angle, car_offset)
    
    # Simulate speed variations (slower in corners)
    corner_slowdown = abs(math.sin(math.radians(angle * 4))) * 0.3
    base_speed = 250 * speed_factor
    speed = base_speed * (1 - corner_slowdown)
    
    # Simulate G-forces
    acceleration_x = math.sin(math.radians(angle * 3)) * 2.5
    acceleration_y = math.cos(math.radians(angle * 2)) * 2.0
    
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
            "heading": angle % 360
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

def run_simulation(duration_seconds=60):
    """Run multi-car simulation"""
    start_time = time.time()
    lap_progress = [0.0, 0.15, 0.3]  # Stagger car positions
    
    iteration = 0
    
    while time.time() - start_time < duration_seconds:
        iteration += 1
        
        for i, car in enumerate(TEST_CARS):
            # Update lap progress (car 01 is fastest)
            speed_multiplier = 1.0 + (i * 0.05)
            lap_progress[i] = (lap_progress[i] + 0.005 * speed_multiplier) % 1.0
            
            # Generate and send telemetry
            telemetry = generate_telemetry(car, lap_progress[i], speed_multiplier)
            
            try:
                response = requests.post(f"{API_URL}/telemetry", json=telemetry)
                if response.status_code == 200:
                    print(f"[T+{iteration:03d}] {car['driver_name']}: {telemetry['motion']['speed']:.1f} km/h at sector {int(lap_progress[i] * 3) + 1}")
            except Exception as e:
                print(f"Error sending telemetry: {e}")
        
        print()  # Blank line between iterations
        time.sleep(0.5)  # Send updates every 500ms

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
        
        # Start flag scenario in background
        flag_thread = threading.Thread(target=trigger_flag_scenario, daemon=True)
        flag_thread.start()
        
        # Run simulation
        run_simulation(duration_seconds=30)
        
        print("\n" + "=" * 60)
        print("SIMULATION COMPLETE")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print("\n\nSimulation stopped by user")
    except Exception as e:
        print(f"\nError: {e}")