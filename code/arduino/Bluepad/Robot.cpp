#include "Robot.h"
#include <Arduino.h>

#ifdef BOARD_M5ATOM
const int SERVO_LEFT_PIN = 21;
const int SERVO_RIGHT_PIN = 25;
#else
// "Base assembly" wiring
const int SERVO_LEFT_PIN = 1;
const int SERVO_RIGHT_PIN = 43;
#endif

#ifdef MOTORS_GEEKSERVO
const int SERVO_US_LOW = 500;
const int SERVO_US_HIGH = 2500;
#else
// SG90 config
const int SERVO_US_LOW = 1000;
const int SERVO_US_HIGH = 2000;
#endif

// The "DC" wiring example
#ifdef MOTORS_DC
const int DCMOTOR_LEFT_PIN_FWD = 9; // D10
const int DCMOTOR_LEFT_PIN_BACK = 8; // D9
const int DCMOTOR_RIGHT_PIN_FWD = 7; // D8
const int DCMOTOR_RIGHT_PIN_BACK = 44; // D7
#endif

inline float clamp(float value, float min, float max) {
  return value < min ? min : value > max ? max : value;
}

void Robot::setup() {
#ifdef MOTORS_DC
  analogWrite(DCMOTOR_LEFT_PIN_BACK, 0);
  analogWrite(DCMOTOR_LEFT_PIN_FWD, 0);
  analogWrite(DCMOTOR_RIGHT_PIN_BACK, 0);
  analogWrite(DCMOTOR_RIGHT_PIN_FWD, 0);
#else
  // Set up ESP32Servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  pwm.attachPin(SERVO_LEFT_PIN, 10000);
  pwm.attachPin(SERVO_RIGHT_PIN, 10000);
  servo_left.setPeriodHertz(50);  // Standard 50hz servo
  servo_left.setPeriodHertz(50);  // Standard 50hz servo
  servo_left.attach(SERVO_LEFT_PIN, SERVO_US_LOW, SERVO_US_HIGH);
  servo_right.attach(SERVO_RIGHT_PIN, SERVO_US_LOW, SERVO_US_HIGH);
#endif

#ifdef BOARD_M5ATOM
  neopixel.begin();
  setLed(64, 0, 0);
#else
  pinMode(LED_BUILTIN, OUTPUT);
#endif
}

void Robot::drive(float left_power, float right_power) {
#ifdef MOTORS_DC
  if (left_power > 0) {
    analogWrite(DCMOTOR_LEFT_PIN_FWD, (int)(clamp(left_power, 0, 1)*255));
    analogWrite(DCMOTOR_LEFT_PIN_BACK, 0);
  }
  else {
    analogWrite(DCMOTOR_LEFT_PIN_BACK, (int)(clamp(-left_power, 0, 1)*255));
    analogWrite(DCMOTOR_LEFT_PIN_FWD, 0);
  }
  if (right_power > 0) {
    analogWrite(DCMOTOR_RIGHT_PIN_FWD, (int)(clamp(right_power, 0, 1)*255));
    analogWrite(DCMOTOR_RIGHT_PIN_BACK, 0);
  }
  else {
    analogWrite(DCMOTOR_RIGHT_PIN_BACK, (int)(clamp(-right_power, 0, 1)*255));
    analogWrite(DCMOTOR_RIGHT_PIN_FWD, 0);
  }
#else
  // Left motor is mounted in reverse
  float left_us =
      (-clamp(left_power, -1, 1) + 1.0) / 2.0 * (SERVO_US_HIGH - SERVO_US_LOW) +
      SERVO_US_LOW;
  float right_us =
      (clamp(right_power, -1, 1) + 1.0) / 2.0 * (SERVO_US_HIGH - SERVO_US_LOW) +
      SERVO_US_LOW;
  servo_left.writeMicroseconds((int)left_us);
  servo_right.writeMicroseconds((int)right_us);
#endif
}

void Robot::driveTT(float throttle, float turn) {
  drive(throttle - turn, throttle + turn);
}

void Robot::setLed(uint8_t r, uint8_t g, uint8_t b) {
#ifdef BOARD_M5ATOM
  neopixel.setPixelColor(0, neopixel.Color(r, g, b));
  neopixel.show();
#else
  if (r > 0) {
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    digitalWrite(LED_BUILTIN, LOW);
  }
#endif
}