#include "wifi-manager.h"
#include "../config/secrets.h"
#include "../config/pins.h"
#include "../config/constants.h"

WiFiManager::WiFiManager() {
    lastReconnectAttempt = 0;
}

void WiFiManager::begin() {
    // Initialize status LED
    pinMode(STATUS_LED_PIN, OUTPUT);
    digitalWrite(STATUS_LED_PIN, LOW);
    
    // Set WiFi mode
    WiFi.mode(WIFI_STA);
    WiFi.setAutoReconnect(true);
}

void WiFiManager::connect() {
    Serial.println("[WiFi] Connecting to WiFi...");
    Serial.print("[WiFi] SSID: ");
    Serial.println(WIFI_SSID);
    
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    
    int attempts = 0;
    while (WiFi.status() != WL_CONNECTED && attempts < 20) {
        delay(500);
        Serial.print(".");
        blinkStatusLED(1);
        attempts++;
    }
    
    if (WiFi.status() == WL_CONNECTED) {
        Serial.println();
        Serial.println("[WiFi] Connected!");
        Serial.print("[WiFi] IP Address: ");
        Serial.println(WiFi.localIP());
        
        // Solid LED when connected
        digitalWrite(STATUS_LED_PIN, HIGH);
    } else {
        Serial.println();
        Serial.println("[WiFi] Connection failed!");
    }
}

bool WiFiManager::isConnected() {
    return WiFi.status() == WL_CONNECTED;
}

void WiFiManager::reconnect() {
    unsigned long currentMillis = millis();
    
    if (currentMillis - lastReconnectAttempt >= WIFI_RETRY_DELAY) {
        lastReconnectAttempt = currentMillis;
        
        Serial.println("[WiFi] Connection lost. Reconnecting...");
        WiFi.disconnect();
        connect();
    }
}

String WiFiManager::getLocalIP() {
    return WiFi.localIP().toString();
}

void WiFiManager::blinkStatusLED(int times) {
    for (int i = 0; i < times; i++) {
        digitalWrite(STATUS_LED_PIN, HIGH);
        delay(100);
        digitalWrite(STATUS_LED_PIN, LOW);
        delay(100);
    }
}