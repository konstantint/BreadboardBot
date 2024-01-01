
#include "HTTPController.h"

#include <esp_err.h>

#include "Arduino.h"
#include "index.html.h"

// We only support a single controller
HTTPController *_singleton_controller = nullptr;

static esp_err_t index_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/html");
  return httpd_resp_send(req, &index_html[0], strlen(&index_html[0]));
}

static esp_err_t steer_handler(httpd_req_t *req) {
  httpd_resp_set_type(req, "text/json");
  int buf_len = httpd_req_get_url_query_len(req) + 1;
  float throttle = 0, turn = 0;
  if (buf_len > 1) {
    char *buf = (char *)malloc(buf_len);
    if (httpd_req_get_url_query_str(req, buf, buf_len) == ESP_OK) {
      char param[10] = {};
      if (httpd_query_key_value(buf, "throttle", param, sizeof(param)) ==
          ESP_OK) {
        throttle = String(param).toFloat();
      } else {
        throttle = 0;
      }
      if (httpd_query_key_value(buf, "turn", param, sizeof(param)) == ESP_OK) {
        turn = String(param).toFloat();
      } else {
        turn = 0;
      }
    }
    free(buf);
  }
  if (_singleton_controller != nullptr) {
    _singleton_controller->callback_(throttle, turn);
  }
  return httpd_resp_send(req, "OK", strlen("OK"));
}

void HTTPController::setup(
    std::function<void(float throttle, float turn)> callback) {
  callback_ = callback;
  _singleton_controller = this;

  httpd_config_t config = HTTPD_DEFAULT_CONFIG();

  httpd_uri_t index_uri = {.uri = "/",
                           .method = HTTP_GET,
                           .handler = index_handler,
                           .user_ctx = NULL};
  httpd_uri_t steer_uri = {.uri = "/steer",
                           .method = HTTP_GET,
                           .handler = steer_handler,
                           .user_ctx = NULL};

  Serial.printf("Starting web server on port: '%d'\n", config.server_port);
  if (httpd_start(&_httpd, &config) == ESP_OK) {
    httpd_register_uri_handler(_httpd, &index_uri);
    httpd_register_uri_handler(_httpd, &steer_uri);
  }
}