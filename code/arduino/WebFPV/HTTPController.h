
#ifndef HTTP_CONTROLLER_H
#define HTTP_CONTROLLER_H
#include <esp_http_server.h>

#include <functional>

class HTTPController {
 public:
  void setup(std::function<void(float throttle, float turn)> callback);

  std::function<void(float throttle, float turn)> callback_;
 private:
  httpd_handle_t _httpd = NULL;
};
#endif