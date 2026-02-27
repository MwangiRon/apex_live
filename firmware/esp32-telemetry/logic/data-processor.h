#ifndef DATA_PROCESSOR_H
#define DATA_PROCESSOR_H

#include <Arduino.h>

struct TelemetryPacket {
    // Position
    float latitude;
    float longitude;
    float altitude;
    float normalized_x;
    float normalized_y;
    
    // Motion
    float speed;
    float acceleration_x;
    float acceleration_y;
    float acceleration_z;
    float heading;
    
    // Sensors
    float temperature_engine;
    float temperature_ambient;
    
    // Metadata
    String device_id;
    String timestamp;
};

class DataProcessor {
public:
    DataProcessor();
    void generateSimulatedData(TelemetryPacket* packet);
    String buildJSON(const TelemetryPacket& packet);
    
private:
    float lapProgress;
    unsigned long lastUpdateTime;
    
    void updateLapProgress();
    void generatePosition(TelemetryPacket* packet);
    void generateMotion(TelemetryPacket* packet);
    void generateSensors(TelemetryPacket* packet);
    String getCurrentTimestamp();
};

#endif