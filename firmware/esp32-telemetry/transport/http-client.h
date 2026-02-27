#ifndef HTTP_CLIENT_H
#define HTTP_CLIENT_H

#include <HTTPClient.h>
#include <ArduinoJson.h>

class TelemetryHTTPClient {
public:
    TelemetryHTTPClient();
    bool sendTelemetry(const String& jsonPayload);
    String getServerURL();
    
private:
    HTTPClient http;
    String buildURL();
};

#endif