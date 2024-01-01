#ifndef ROBOT_H
#define ROBOT_H
#include "config.h"
#include <ESP32Servo.h>

class Robot {
 public:
  void setup();
  void drive(float left, float right);
  void driveTT(float throttle, float turn);
  void setLed(uint8_t r, uint8_t g, uint8_t b);

 private:
  Servo servo_left;
  Servo servo_right;
  ESP32PWM pwm;
};
#endif