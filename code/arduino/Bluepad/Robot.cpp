#include "Robot.h"

#ifdef M5ATOM
int SERVO_LEFT_PIN = 21;
int SERVO_RIGHT_PIN = 25;
#else
int SERVO_LEFT_PIN = 1;
int SERVO_RIGHT_PIN = 43;
#endif

int SERVO_US_LOW = 1000;
int SERVO_US_HIGH = 2000;

inline float clamp(float value, float min, float max) {
  return value < min ? min : value > max ? max : value;
}

void Robot::setup() {
  // Set up ESP32Servo
  ESP32PWM::allocateTimer(0);
  ESP32PWM::allocateTimer(1);
  pwm.attachPin(SERVO_LEFT_PIN, 10000);
  pwm.attachPin(SERVO_RIGHT_PIN, 10000);
  servo_left.setPeriodHertz(50);  // Standard 50hz servo
  servo_left.setPeriodHertz(50);  // Standard 50hz servo
  servo_left.attach(SERVO_LEFT_PIN, SERVO_US_LOW, SERVO_US_HIGH);
  servo_right.attach(SERVO_RIGHT_PIN, SERVO_US_LOW, SERVO_US_HIGH);

#ifdef M5ATOM
  neopixel.begin();
  setLed(64, 0, 0);
#else
  pinMode(LED_BUILTIN, OUTPUT);
#endif
}

void Robot::drive(float left_power, float right_power) {
  // Left motor is mounted in reverse
  float left_us =
      (-clamp(left_power, -1, 1) + 1.0) / 2.0 * (SERVO_US_HIGH - SERVO_US_LOW) +
      SERVO_US_LOW;
  float right_us =
      (clamp(right_power, -1, 1) + 1.0) / 2.0 * (SERVO_US_HIGH - SERVO_US_LOW) +
      SERVO_US_LOW;
  servo_left.writeMicroseconds((int)left_us);
  servo_right.writeMicroseconds((int)right_us);
}

void Robot::driveTT(float throttle, float turn) {
  drive(throttle - turn, throttle + turn);
}

void Robot::setLed(uint8_t r, uint8_t g, uint8_t b) {
#ifdef M5ATOM
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