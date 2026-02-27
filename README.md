# F1 Telemetry Project

Real-time Formula 1 telemetry system with multi-car tracking, race control, and live visualization.

## System Overview

A full-stack telemetry platform consisting of:
- **Backend**: Python FastAPI with WebSocket support
- **Frontend**: React + TypeScript with real-time updates
- **Simulation**: ESP32-compatible firmware (simulation mode)

## Features

### Core Telemetry
- [x] Real-time GPS position tracking
- [x] Speed and G-force monitoring
- [x] Engine and ambient temperature sensors
- [x] Coordinate normalization (GPS to track coordinates)
- [x] WebSocket streaming for live updates

### Multi-Car Support
- [x] Track up to 11 cars simultaneously
- [x] F1 2026 team colors and branding
- [x] Individual car trails and position markers
- [x] Per-car telemetry data streams

### Race Control System
- [x] Flag management (Green, Yellow, Double Yellow, Red, Blue, Black)
- [x] Full course and sector-specific flags
- [x] Visual flag animations on track display
- [x] Real-time flag state broadcasting

### Track Visualization
- [x] Red Bull Ring circuit layout with 10 corners
- [x] Sector boundaries (S1, S2, S3)
- [x] Start/Finish line marker
- [x] Live car position with heading indicators
- [x] Team-colored car markers and trails

### Session Management
- [x] Session state tracking
- [x] Active car registration
- [x] Lap progress monitoring

## Tech Stack

### Backend
- FastAPI 0.109.0
- Python 3.8+
- WebSockets for real-time communication
- Pydantic for data validation
- Uvicorn ASGI server

### Frontend
- React 18
- TypeScript
- Vite (build tool)
- Tailwind CSS
- HTML5 Canvas for track visualization
- Lucide React icons

### Hardware (Optional)
- ESP32 Dev Module
- Compatible with simulation mode (no physical hardware required)

## Project Structure
```
f1-telemetry-project/
├── backend/                 # FastAPI server
│   ├── app/
│   │   ├── models/          # Data models (telemetry, car, session)
│   │   ├── logic/           # Business logic (race control, coordinates)
│   │   ├── transport/       # API endpoints and WebSocket handlers
│   │   └── utils/           # Utilities and helpers
│   ├── tests/               # Backend tests
│   └── requirements.txt
│
├── frontend/                # React application
│   ├── src/
│   │   ├── components/      # UI components
│   │   ├── hooks/           # Custom React hooks
│   │   ├── services/        # API and WebSocket clients
│   │   └── types/           # TypeScript definitions
│   └── package.json
│
├── firmware/                # ESP32 firmware (simulation mode)
│   └── esp32-telemetry/
│       ├── config/          # WiFi credentials, pins, constants
│       ├── logic/           # Data processing
│       └── transport/       # HTTP client, WiFi manager
│
├── shared/                  # Shared schemas
│   └── schemas/
│       └── telemetry.schema.json
│
└── docs/                    # Documentation
    └── architecture.md
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

### 1. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.template .env

# Start server
python -m uvicorn app.main:app --reload
```

Backend will run on: http://localhost:8000

API Documentation: http://localhost:8000/docs

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.template .env

# Start development server
npm run dev
```

Frontend will run on: http://localhost:5173

### 3. Run Simulation
```bash
cd backend

# Start multi-car simulation
python generate_test_data.py
```

This simulates 3 cars (Verstappen, Leclerc, Russell) racing around Red Bull Ring.

## API Endpoints

### Telemetry
- `POST /api/v1/telemetry` - Submit telemetry data
- `GET /api/v1/telemetry/latest` - Get recent telemetry

### Track Information
- `GET /api/v1/track/info` - Track details
- `GET /api/v1/track/layout` - Track waypoints

### Car Management
- `POST /api/v1/cars/register` - Register a car
- `GET /api/v1/cars/teams` - List F1 teams

### Session Control
- `POST /api/v1/session/start` - Start race session
- `GET /api/v1/session/status` - Current session state

### Flag Control
- `POST /api/v1/flags/set` - Change flag state
- `GET /api/v1/flags/current` - Current flag

### WebSocket
- `ws://localhost:8000/ws/telemetry` - Real-time data stream

## F1 2026 Teams

Supported teams with official colors:
- Oracle Red Bull Racing
- Scuderia Ferrari HP
- Mercedes-AMG PETRONAS F1 Team
- McLaren Mastercard F1 Team
- Aston Martin Aramco F1 Team
- BWT Alpine F1 Team
- Atlassian Williams F1 Team
- Visa Cash App Racing Bulls F1 Team
- Audi Revolut F1 Team
- TGR Haas F1 Team
- Cadillac F1 Team

## Configuration

### Backend (.env)
```env
HOST=0.0.0.0
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000/ws/telemetry
```

### ESP32 (secrets.h)
```cpp
#define WIFI_SSID "your-wifi-name"
#define WIFI_PASSWORD "your-wifi-password"
#define API_HOST "192.168.1.100"
#define DEVICE_ID "esp32-car-01"
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Test Scripts
```bash
# Race control system
python test_race_control.py

# WebSocket flags
python test_websocket_flags.py

# Red Bull Ring simulation
python test_redbull_ring.py
```

## Development

### Adding a New Car
```bash
# Edit backend/generate_test_data.py
TEST_CARS.append({
    "device_id": "esp32-car-04",
    "car_number": 44,
    "driver_name": "Lewis Hamilton",
    "team": "mercedes"
})
```

### Changing Track
Update waypoints in `backend/app/logic/coordinate_normalizer.py`

### Custom Flag Scenario
```python
requests.post("http://localhost:8000/api/v1/flags/set", json={
    "flag_type": "yellow",
    "full_course": False,
    "sectors": ["sector_2"],
    "message": "Incident at Turn 4"
})
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version` (need 3.8+)
- Verify virtual environment is activated
- Check port 8000 is available

### Frontend won't connect
- Ensure backend is running first
- Check CORS settings in backend .env
- Verify WebSocket URL in frontend .env

### Simulation not showing cars
- Confirm session started: `curl http://localhost:8000/api/v1/session/status`
- Check backend logs for errors
- Verify track layout loads: `curl http://localhost:8000/api/v1/track/layout`

## Future Enhancements

### Planned Features
- [ ] Lap timing system with sector times
- [ ] Leaderboard and race positions
- [ ] Historical data playback
- [ ] Database persistence (PostgreSQL)
- [ ] MQTT transport layer
- [ ] Real sensor integration (GPS, IMU)
- [ ] Smooth corner curves (spline interpolation)
- [ ] Sound effects for flag changes
- [ ] Mobile-responsive design

## License

MIT License - See LICENSE file

## Contributing

This is a student project. Contributions and forks are welcome!

## Acknowledgments

- Red Bull Ring circuit data
- F1 2026 team color specifications