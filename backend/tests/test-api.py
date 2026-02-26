from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test health check endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "online"
    assert "Red Bull Ring" in data["track"]


def test_track_info():
    """Test track info endpoint"""
    response = client.get("/api/v1/track/info")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Red Bull Ring"
    assert data["location"] == "Spielberg, Austria"
    assert data["length_km"] == 4.318


def test_post_telemetry_redbull_ring():
    """Test posting telemetry data from Red Bull Ring"""
    # Coordinates near Turn 1 (Castrol Edge)
    telemetry = {
        "device_id": "esp32-redbull-01",
        "position": {
            "latitude": 47.2207,  # Near Turn 1
            "longitude": 14.7625,
            "altitude": 678.0  # Red Bull Ring elevation ~670m
        },
        "motion": {
            "speed": 285.5,  # High speed on main straight
            "heading": 180.0,
            "acceleration_x": 0.5,
            "acceleration_y": 2.1,
            "acceleration_z": -0.2
        },
        "sensors": {
            "temperature_engine": 98.5,
            "temperature_ambient": 24.0
        }
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry)
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "esp32-redbull-01"
    assert "normalized_x" in data["position"]
    assert "normalized_y" in data["position"]
    
    # Verify coordinates are in valid range
    assert 0 <= data["position"]["normalized_x"] <= 1000
    assert 0 <= data["position"]["normalized_y"] <= 1000


def test_get_latest_telemetry():
    """Test retrieving latest telemetry"""
    response = client.get("/api/v1/telemetry/latest?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_filter_by_device():
    """Test filtering telemetry by device ID"""
    response = client.get("/api/v1/telemetry/latest?device_id=esp32-redbull-01&limit=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)