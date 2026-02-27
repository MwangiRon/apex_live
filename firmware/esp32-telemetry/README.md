# ESP32 Telemetry Firmware

## Arduino IDE Setup

### 1. Install ESP32 Board Support
- Open Arduino IDE
- File -> Preferences
- Add to "Additional Board Manager URLs":
```
  https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
- Tools -> Board -> Board Manager
- Search "ESP32" and install "esp32 by Espressif Systems"

### 2. Install Libraries
- Sketch -> Include Library -> Manage Libraries
- Search and install:
  - ArduinoJson by Benoit Blanchon (version 6.x)

### 3. Configure Board
- Tools -> Board -> ESP32 Arduino -> ESP32 Dev Module
- Tools -> Upload Speed -> 921600
- Tools -> Port -> Select your ESP32 port

### 4. Configure Secrets
- Copy `config/secrets.h.template` to `config/secrets.h`
- Edit with your WiFi credentials and API endpoint

### 5. Upload
- Click Upload button
- Open Serial Monitor (115200 baud)
```

---

## Verify File Structure

Your complete firmware structure:
```
firmware/esp32-telemetry/
├── esp32-telemetry.ino
├── platformio.ini
├── README.md
├── config/
│   ├── secrets.h.template
│   ├── secrets.h
│   ├── pins.h
│   └── constants.h
├── transport/
│   ├── wifi-manager.h
│   ├── wifi-manager.cpp
│   ├── http-client.h
│   └── http-client.cpp
└── logic/
    ├── data-processor.h
    └── data-processor.cpp