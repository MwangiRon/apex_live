#ifndef CONSTANTS_H
#define CONSTANTS_H

// Simulation Mode
#define SIMULATION_MODE true

// Timing Configuration
#define SENSOR_READ_INTERVAL 100    // Read sensors every 100ms
#define PUBLISH_INTERVAL 500        // Publish data every 500ms
#define WIFI_RETRY_DELAY 5000       // Retry WiFi every 5 seconds

// Red Bull Ring Track Configuration
#define TRACK_CENTER_LAT 47.2197
#define TRACK_CENTER_LON 14.7647
#define TRACK_WIDTH_METERS 1500.0
#define TRACK_HEIGHT_METERS 2000.0

// Simulation Parameters
#define SIM_BASE_SPEED 250.0        // Base speed in km/h
#define SIM_LAP_TIME_SECONDS 90.0   // Time for one lap
#define SIM_TRACK_RADIUS 0.01       // Track radius in degrees

#endif