#include "http-client.h"
#include "../config/secrets.h"

TelemetryHTTPClient::TelemetryHTTPClient() {
}

String TelemetryHTTPClient::buildURL() {
    String url = "http://";
    url += API_HOST;
    url += ":";
    url += String(API_PORT);
    url += API_ENDPOINT;
    return url;
}

String TelemetryHTTPClient::getServerURL() {
    return buildURL();
}

bool TelemetryHTTPClient::sendTelemetry(const String& jsonPayload) {
    String url = buildURL();
    
    http.begin(url);
    http.addHeader("Content-Type", "application/json");
    
    int httpResponseCode = http.POST(jsonPayload);
    
    if (httpResponseCode > 0) {
        Serial.print("[HTTP] Response code: ");
        Serial.println(httpResponseCode);
        
        if (httpResponseCode == 200) {
            Serial.println("[HTTP] Telemetry sent successfully");
            http.end();
            return true;
        }
    } else {
        Serial.print("[HTTP] Error: ");
        Serial.println(http.errorToString(httpResponseCode));
    }
    
    http.end();
    return false;
}