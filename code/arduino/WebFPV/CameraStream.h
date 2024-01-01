#ifndef CAMERA_STREAM_H
#define CAMERA_STREAM_H
#include <esp_http_server.h>

// Sets up a HTTP streaming server to stream camera
// images over port 81
class CameraStream {
 public:
  void setup();

 private:
  httpd_handle_t _httpd = NULL;
};

#endif