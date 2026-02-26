"""
Manual test script to verify Red Bull Ring coordinate normalization
"""
import requests
import json
from datetime import datetime


API_URL = "http://localhost:8000/api/v1"


def test_track_info():
    """Display track information"""
    response = requests.get(f"{API_URL}/track/info")
    print("=" * 60)
    print("RED BULL RING TRACK INFO")
    print("=" * 60)
    print(json.dumps(response.json(), indent=2))
    print()


def test_coordinate_normalization():
    """Test coordinate normalization at key track points"""
    print("=" * 60)
    print("COORDINATE NORMALIZATION TEST")
    print("=" * 60)
    
    test_points = [
        {
            "name": "Start/Finish Line",
            "lat": 47.2197,
            "lon": 14.7620
        },
        {
            "name": "Turn 1 (Castrol Edge)",
            "lat": 47.2207,
            "lon": 14.7625
        },
        {
            "name": "Turn 3 (Remus)",
            "lat": 47.2220,
            "lon": 14.7650
        },
        {
            "name": "Turn 4 (Schlossgold)",
            "lat": 47.2210,
            "lon": 14.7670
        }
    ]
    
    for point in test_points:
        telemetry = {
            "device_id": "test-device",
            "position": {
                "latitude": point["lat"],
                "longitude": point["lon"],
                "altitude": 678.0
            },
            "motion": {
                "speed": 250.0,
                "heading": 90.0
            }
        }
        
        response = requests.post(f"{API_URL}/telemetry", json=telemetry)
        data = response.json()
        
        print(f"\n{point['name']}:")
        print(f"  GPS: ({point['lat']:.4f}, {point['lon']:.4f})")
        print(f"  Normalized: ({data['position']['normalized_x']:.2f}, {data['position']['normalized_y']:.2f})")


def test_live_telemetry():
    """Send a realistic telemetry packet"""
    print("\n" + "=" * 60)
    print("LIVE TELEMETRY TEST")
    print("=" * 60)
    
    telemetry = {
        "device_id": "esp32-redbull-car-01",
        "position": {
            "latitude": 47.2197,
            "longitude": 14.7647,
            "altitude": 678.0
        },
        "motion": {
            "speed": 287.5,
            "acceleration_x": 1.8,
            "acceleration_y": 2.4,
            "acceleration_z": -0.3,
            "heading": 145.0
        },
        "sensors": {
            "temperature_engine": 96.8,
            "temperature_ambient": 22.5
        }
    }
    
    response = requests.post(f"{API_URL}/telemetry", json=telemetry)
    print("\nSent telemetry packet:")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    try:
        print("\n🏁 RED BULL RING TELEMETRY SYSTEM TEST 🏁\n")
        
        test_track_info()
        test_coordinate_normalization()
        test_live_telemetry()
        
        print("\n" + "=" * 60)
        print("✅ All tests completed successfully!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to API server")
        print("Make sure the server is running: python -m uvicorn app.main:app --reload")
    except Exception as e:
        print(f"❌ Error: {e}")