import requests
import json

API_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("RACE CONTROL SYSTEM TEST")
print("=" * 60)

# 1. Start session
print("\n1. Starting session...")
response = requests.post(f"{API_URL}/session/start?session_id=test-race&session_type=race")
print(json.dumps(response.json(), indent=2))

# 2. Get available teams
print("\n2. Available F1 teams:")
response = requests.get(f"{API_URL}/cars/teams")
teams = response.json()["teams"]
for team_id, team_info in teams.items():
    print(f"  {team_info['name']}: {team_info['primary']}")

# 3. Register a car
print("\n3. Registering Max Verstappen...")
car_data = {
    "device_id": "esp32-car-01",
    "car_number": 1,
    "driver_name": "Max Verstappen",
    "team": "red_bull",
    "team_colors": teams["red_bull"]
}
response = requests.post(f"{API_URL}/cars/register", json=car_data)
print(json.dumps(response.json(), indent=2))

# 4. Set yellow flag in sector 2
print("\n4. Setting YELLOW flag in Sector 2...")
flag_data = {
    "flag_type": "yellow",
    "full_course": False,
    "sectors": ["sector_2"],
    "message": "Incident at Turn 4"
}
response = requests.post(f"{API_URL}/flags/set", json=flag_data)
print(json.dumps(response.json(), indent=2))

# 5. Check session status
print("\n5. Current session status:")
response = requests.get(f"{API_URL}/session/status")
print(json.dumps(response.json(), indent=2))

print("\n" + "=" * 60)
print("✅ Race control test complete!")
print("=" * 60)