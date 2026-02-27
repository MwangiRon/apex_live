#include "data-processor.h"
#include "../config/secrets.h"
#include "../config/constants.h"
#include <math.h>
#include <time.h>

DataProcessor::DataProcessor() {
    lapProgress = 0.0;
    lastUpdateTime = millis();
}

void DataProcessor::updateLapProgress() {
    unsigned long currentTime = millis();
    unsigned long deltaTime = currentTime - lastUpdateTime;
    lastUpdateTime = currentTime;
    
    // Calculate progress based on lap time
    float progressPerSecond = 1.0 / SIM_LAP_TIME_SECONDS;
    float progressIncrement = progressPerSecond * (deltaTime / 1000.0);
    
    lapProgress += progressIncrement;
    if (lapProgress >= 1.0) {
        lapProgress = 0.0;
        Serial.println("[SIM] Lap completed!");
    }
}

void DataProcessor::generatePosition(TelemetryPacket* packet) {
    // Convert lap progress to angle (0-360 degrees)
    float angle = lapProgress * 360.0;
    float angleRad = angle * (PI / 180.0);
    
    // Generate circular GPS coordinates
    packet->latitude = TRACK_CENTER_LAT + (SIM_TRACK_RADIUS * cos(angleRad));
    packet->longitude = TRACK_CENTER_LON + (SIM_TRACK_RADIUS * sin(angleRad));
    packet->altitude = 678.0;
    
    // Normalized coordinates will be calculated by backend
    packet->normalized_x = 0.0;
    packet->normalized_y = 0.0;
}

void DataProcessor::generateMotion(TelemetryPacket* packet) {
    float angle = lapProgress * 360.0;
    
    // Simulate speed variations (slower in corners)
    float cornerSlowdown = abs(sin((angle * 4.0) * (PI / 180.0))) * 0.3;
    packet->speed = SIM_BASE_SPEED * (1.0 - cornerSlowdown);
    
    // Simulate G-forces
    packet->acceleration_x = sin((angle * 3.0) * (PI / 180.0)) * 2.5;
    packet->acceleration_y = cos((angle * 2.0) * (PI / 180.0)) * 2.0;
    packet->acceleration_z = -0.2;
    
    // Heading follows track
    packet->heading = fmod(angle, 360.0);
}

void DataProcessor::generateSensors(TelemetryPacket* packet) {
    // Engine temperature varies with speed
    packet->temperature_engine = 85.0 + (packet->speed / 250.0) * 15.0;
    
    // Ambient temperature
    packet->temperature_ambient = 22.5;
}

String DataProcessor::getCurrentTimestamp() {
    // Simple timestamp (can be improved with RTC)
    unsigned long ms = millis();
    return String(ms);
}

void DataProcessor::generateSimulatedData(TelemetryPacket* packet) {
    updateLapProgress();
    
    packet->device_id = String(DEVICE_ID);
    packet->timestamp = getCurrentTimestamp();
    
    generatePosition(packet);
    generateMotion(packet);
    generateSensors(packet);
    
    Serial.print("[SIM] Lap Progress: ");
    Serial.print(lapProgress * 100.0, 1);
    Serial.print("% | Speed: ");
    Serial.print(packet->speed, 1);
    Serial.println(" km/h");
}

String DataProcessor::buildJSON(const TelemetryPacket& packet) {
    String json = "{";
    
    // Device ID
    json += "\"device_id\":\"" + packet.device_id + "\",";
    
    // Position
    json += "\"position\":{";
    json += "\"latitude\":" + String(packet.latitude, 6) + ",";
    json += "\"longitude\":" + String(packet.longitude, 6) + ",";
    json += "\"altitude\":" + String(packet.altitude, 1);
    json += "},";
    
    // Motion
    json += "\"motion\":{";
    json += "\"speed\":" + String(packet.speed, 1) + ",";
    json += "\"acceleration_x\":" + String(packet.acceleration_x, 2) + ",";
    json += "\"acceleration_y\":" + String(packet.acceleration_y, 2) + ",";
    json += "\"acceleration_z\":" + String(packet.acceleration_z, 2) + ",";
    json += "\"heading\":" + String(packet.heading, 1);
    json += "},";
    
    // Sensors
    json += "\"sensors\":{";
    json += "\"temperature_engine\":" + String(packet.temperature_engine, 1) + ",";
    json += "\"temperature_ambient\":" + String(packet.temperature_ambient, 1);
    json += "}";
    
    json += "}";
    
    return json;
}