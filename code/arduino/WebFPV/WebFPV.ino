
#include <ESPmDNS.h>
#include <WiFi.h>

#include "CameraStream.h"
#include "HTTPController.h"
#include "Robot.h"

HTTPController controller;
CameraStream camera_stream;
Robot robot;

void setupMDNS() {
  if (!MDNS.begin("breadboardbot")) {
    Serial.println("Error setting up MDNS responder!");
  }
  MDNS.addService("http", "tcp", 80);
}

void setupWifi(bool access_point = true, const char* ssid = "",
               const char* password = "") {
  if (!access_point) {
    // Connect to existing network
    WiFi.begin(ssid, password);
    WiFi.setSleep(false);

    while (WiFi.status() != WL_CONNECTED) {
      delay(500);
      Serial.print(".");
    }
    Serial.println("");
    Serial.println("WiFi connected");
    Serial.print("Address: ");
    Serial.println(WiFi.localIP());
  } else {
    // Set up an AP
    WiFi.softAP("BreadboardBotFPV");
    // delay(1000);
    // Configure a non-192.168.4.1 IP:
    // WiFi.softAPConfig({10, 1, 1, 1}, {10, 1, 1, 1}, {255, 255, 255, 0});
    Serial.print("AP IP address: http://");
    Serial.println(WiFi.softAPIP());
  }
}

void setup() {
  Serial.begin(115200);
  // To connect to your local network:
  // setupWifi(false, "<SSID>", "<password>");
  // To set up a BreadboardBotFPV access point
  setupWifi();
  // Note that the AP mode seems to be less reliable:
  //  - mDNS does not work somewhy (you have to connect to 192.168.4.1,
  //         not breadboardbot.local)
  //  - Some smartphones outright refuse to connect to 192.168.4.1 while in the
  //  AP network somewhy.
  robot.setup();
  controller.setup(
      [&robot](float throttle, float turn) { robot.driveTT(throttle, turn); });
  camera_stream.setup();
  setupMDNS();
}

void loop() {}
