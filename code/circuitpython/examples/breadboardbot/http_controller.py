from adafruit_httpserver import (
    REQUEST_HANDLED_RESPONSE_SENT,
    Request,
    Response,
    FileResponse,
)


class BasicHTTPListener:
    def __init__(self, server, handler_fn):
        self.server = server
        self.handler_fn = handler_fn

        @self.server.route("/left")
        @self.server.route("/right")
        @self.server.route("/forward")
        @self.server.route("/backward")
        @self.server.route("/stop")
        def action(request: Request):
            return Response(request, self.handler_fn(request))

    def __call__(self, robot):
        try:
            pool_result = self.server.poll()
            if pool_result == REQUEST_HANDLED_RESPONSE_SENT:
                pass
        except OSError as error:
            print(error)
