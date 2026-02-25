from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test health check endpoint"""
    response = client.get("/api/v1/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"


def test_post_telemetry():
    """Test posting telemetry data"""
    telemetry = {
        "device_id": "test-device-01",
        "position": {
            "latitude": 52.0786,
            "longitude": -1.0169,
            "altitude": 150.0
        },
        "motion": {
            "speed": 200.5,
            "heading": 45.0
        }
    }
    
    response = client.post("/api/v1/telemetry", json=telemetry)
    assert response.status_code == 200
    data = response.json()
    assert data["device_id"] == "test-device-01"
    assert "normalized_x" in data["position"]
    assert "normalized_y" in data["position"]


def test_get_latest_telemetry():
    """Test retrieving latest telemetry"""
    response = client.get("/api/v1/telemetry/latest?limit=5")
    assert response.status_code == 200
    assert isinstance(response.json(), list)