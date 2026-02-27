#include "config/secrets.h"
#include "config/pins.h"
#include "config/constants.h"
#include "transport/wifi-manager.h"
#include "transport/http-client.h"
#include "logic/data-processor.h"

// Global objects
WiFiManager wifiManager;
TelemetryHTTPClient httpClient;
DataProcessor dataProcessor;

// Timing variables
unsigned long lastSensorRead = 0;
unsigned long lastPublish = 0;

void setup() {
    // Initialize serial communication
    Serial.begin(115200);
    delay(1000);
    
    Serial.println("========================================");
    Serial.println("F1 TELEMETRY SYSTEM - ESP32");
    Serial.println("========================================");
    Serial.print("Device ID: ");
    Serial.println(DEVICE_ID);
    Serial.print("Mode: ");
    Serial.println(SIMULATION_MODE ? "SIMULATION" : "REAL SENSORS");
    Serial.println("========================================");
    
    // Initialize WiFi
    wifiManager.begin();
    wifiManager.connect();
    
    if (wifiManager.isConnected()) {
        Serial.println("[INIT] System ready!");
        Serial.print("[INIT] Sending data to: ");
        Serial.println(httpClient.getServerURL());
    } else {
        Serial.println("[ERROR] WiFi connection failed!");
        Serial.println("[ERROR] Check secrets.h configuration");
    }
    
    Serial.println("========================================");
    Serial.println();
}

void loop() {
    unsigned long currentMillis = millis();
    
    // Check WiFi connection
    if (!wifiManager.isConnected()) {
        wifiManager.reconnect();
        return;
    }
    
    // Publish telemetry at configured interval
    if (currentMillis - lastPublish >= PUBLISH_INTERVAL) {
        lastPublish = currentMillis;
        
        // Generate telemetry data
        TelemetryPacket packet;
        
        if (SIMULATION_MODE) {
            dataProcessor.generateSimulatedData(&packet);
        } else {
            // TODO: Read real sensors
            Serial.println("[ERROR] Real sensor mode not implemented yet");
            return;
        }
        
        // Build JSON payload
        String jsonPayload = dataProcessor.buildJSON(packet);
        
        // Send to backend
        bool success = httpClient.sendTelemetry(jsonPayload);
        
        if (success) {
            Serial.println("[SUCCESS] Telemetry published");
        } else {
            Serial.println("[ERROR] Failed to publish telemetry");
        }
        
        Serial.println();
    }
    
    // Small delay to prevent watchdog issues
    delay(10);
}