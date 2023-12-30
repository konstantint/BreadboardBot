#include "BluepadController.h"
#include "Robot.h"

Robot robot;
BluepadController controller;

void setup() {
  Serial.begin(115200);
  robot.setup();
  controller.setup(robot);
}

void loop() {
  controller.update(robot);
  vTaskDelay(1);
}
