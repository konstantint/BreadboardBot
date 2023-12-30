#include "BluepadController.h"

// This callback gets called any time a new gamepad is connected.
// Copy-paste from BluePad example, updated to only work with 1 controller at a
// time.
void BluepadController::onConnectedController(ControllerPtr ctl) {
  if (_connectedController != nullptr) {
    Serial.println("ERROR: Cannot connect a second controller!");
    _robot->setLed(0, 64, 64);
  } else {
    Serial.printf("CALLBACK: Controller is connected");
    ControllerProperties properties = ctl->getProperties();
    Serial.printf("Controller model: %s, VID=0x%04x, PID=0x%04x\n",
                  ctl->getModelName().c_str(), properties.vendor_id,
                  properties.product_id);
    _connectedController = ctl;
    BP32.enableNewBluetoothConnections(false);
    _robot->setLed(0, 64, 0);
  }
}

void BluepadController::onDisconnectedController(ControllerPtr ctl) {
  _robot->driveTT(0, 0);
  if (_connectedController != ctl) {
    Serial.println("ERROR: Unknown controller disconnected!");
    _robot->setLed(0, 0, 64);
  } else {
    Serial.printf("CALLBACK: Controller disconnected");
    _robot->setLed(64, 0, 0);
    _connectedController = nullptr;
  }
  BP32.enableNewBluetoothConnections(true);
}

void BluepadController::setup(Robot& robot) {
  _robot = &robot;
  Serial.printf(BP32.firmwareVersion());
  const uint8_t* addr = BP32.localBdAddress();
  Serial.printf("BD Addr: %2X:%2X:%2X:%2X:%2X:%2X\n", addr[0], addr[1], addr[2],
                addr[3], addr[4], addr[5]);
  // "forgetBluetoothKeys()" should be called when the user performs
  // a "device factory reset", or similar.
  // Calling "forgetBluetoothKeys" in setup() just as an example.
  // Forgetting Bluetooth keys prevents "paired" gamepads to reconnect.
  // But might also fix some connection / re-connection issues.
  BP32.forgetBluetoothKeys();
  BP32.setup(
      [this](ControllerPtr ctl) { this->onConnectedController(ctl); },
      [this](ControllerPtr ctl) { this->onDisconnectedController(ctl); });
}

void BluepadController::update(Robot& robot) {
  BP32.update();
  if (_connectedController && _connectedController->isConnected()) {
    if (_connectedController->isGamepad()) {
      int x = _connectedController->axisRX();  // (-511 - 512) right X Axis
      int y = _connectedController->axisY();   // (-511 - 512) left Y axis
      robot.driveTT(y / 512.0, x / 512.0);
    }
  }
}
