# System Architecture

## Overview

Three-tier telemetry system with edge computing on ESP32 devices.

## Data Flow
```
[ESP32 Sensors] → [Logic: Normalize] → [Transport: MQTT/WebSocket]
                                              ↓
[Backend: MQTT] → [Logic: Analyze] → [Storage + WebSocket Broadcast]
                                              ↓
[Frontend: WebSocket] ← [Logic: Transform] ← [Display Components]
```

## Design Principles

1. **Separation of Concerns**: Logic ≠ Transport
2. **Shared Coordinate System**: Same math across all layers
3. **Security**: No hardcoded credentials
4. **Scalability**: Support multiple devices
5. **Simplicity**: Flat folder structure

## Tech Stack

### Backend
- FastAPI (async Python web framework)
- WebSockets for real-time data
- MQTT for device communication
- PostgreSQL (future: data persistence)

### Frontend
- React 18 + TypeScript
- Vite (build tool)
- WebSocket client for live data
- Chart.js or Recharts for visualization

### Firmware
- ESP32 (Arduino framework)
- PlatformIO (build system)
- MQTT publisher
- Sensor libraries: GPS, IMU, Temperature

## Security Model

- Environment variables for backend secrets
- `secrets.h` template for ESP32 credentials
- All secret files in `.gitignore`
- HTTPS/WSS in production

## Future Enhancements

- [ ] Database persistence
- [ ] Historical lap comparison
- [ ] Multi-car session support
- [ ] Predictive analytics