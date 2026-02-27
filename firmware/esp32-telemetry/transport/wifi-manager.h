#ifndef WIFI_MANAGER_H
#define WIFI_MANAGER_H

#include <WiFi.h>

class WiFiManager {
public:
    WiFiManager();
    void begin();
    void connect();
    bool isConnected();
    void reconnect();
    String getLocalIP();
    
private:
    unsigned long lastReconnectAttempt;
    void blinkStatusLED(int times);
};

#endif