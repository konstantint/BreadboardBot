#ifndef BLUEPAD_CONTROLLER_H
#define BLUEPAD_CONTROLLER_H
#include <Bluepad32.h>

#include "Robot.h"

class BluepadController {
 public:
  void setup(Robot& robot);
  void update(Robot& robot);

  // Interface with the BluePad library
  void onConnectedController(ControllerPtr ctl);
  void onDisconnectedController(ControllerPtr ctl);

 private:
  Robot* _robot;
  ControllerPtr _connectedController;
};
#endif