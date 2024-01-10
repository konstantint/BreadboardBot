#ifndef ROBOT_H
#define ROBOT_H
#include "config.h"
#include <stdint.h>

#ifdef BOARD_M5ATOM
#include <Adafruit_NeoPixel.h>
#endif

#ifndef MOTORS_DC
#include <ESP32Servo.h>
#endif

class Robot {
 public:
  void setup();
  void drive(float left, float right);
  void driveTT(float throttle, float turn);
  void setLed(uint8_t r, uint8_t g, uint8_t b);

 private:
#ifndef MOTORS_DC
  Servo servo_left;
  Servo servo_right;
  ESP32PWM pwm;
#endif

#ifdef BOARD_M5ATOM
  Adafruit_NeoPixel neopixel = Adafruit_NeoPixel(
      /* num_pixels=*/1, /* pin=*/27, NEO_GRB + NEO_KHZ800);
#endif
};
#endif