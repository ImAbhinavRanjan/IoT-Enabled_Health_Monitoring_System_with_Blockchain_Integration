#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"

#define WIFI_SSID "Your Wi-Fi Name"         // Your Wi-Fi SSID
#define WIFI_PASSWORD "Wi-Fi Password"       // Your Wi-Fi Password
#define REPORTING_PERIOD_MS 1000       // Report every 1 second

PulseOximeter pox;
float pulseRate = 0.0;
float bloodOxygen = 0.0;
WebServer server(80);                  // Start server on port 80
uint32_t tsLastReport = 0;

void onBeatDetected() {
    Serial.println("Beat detected!");
}

// Serve pulse and oxygen data as JSON
void handleRoot() {
    String jsonResponse = "{\"pulse_rate\":" + String(pulseRate) + ",\"blood_oxygen\":" + String(bloodOxygen) + "}";
    server.send(200, "application/json", jsonResponse);
}

void setup() {
    Serial.begin(115200);
    Serial.println("Initializing...");

    // Connect to Wi-Fi
    WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi! IP address: ");
    Serial.println(WiFi.localIP());

    // Initialize the PulseOximeter instance
    if (!pox.begin()) {
        Serial.println("Failed to initialize MAX30100 sensor!");
        while (1);
    } else {
        Serial.println("MAX30100 sensor initialized successfully!");
    }

    // Set IR LED current for heart rate/SpO2 sensing
    pox.setIRLedCurrent(MAX30100_LED_CURR_7_6MA);
    pox.setOnBeatDetectedCallback(onBeatDetected);

    // Start the server and define the root URL
    server.on("/", handleRoot);
    server.begin();
}

void loop() {
    // Update the sensor readings
    pox.update();

    // Report the readings every second
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        pulseRate = pox.getHeartRate();
        bloodOxygen = pox.getSpO2();

        // Print readings to Serial Monitor
        Serial.print("Heart rate (BPM): ");
        Serial.print(pulseRate);
        Serial.print("    SpO2 (%): ");
        Serial.println(bloodOxygen);

        tsLastReport = millis();
    }

    // Handle incoming client requests
    server.handleClient();
}
