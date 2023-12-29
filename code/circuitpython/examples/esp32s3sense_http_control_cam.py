# ESP32S3 robot control via HTTP with a real-time web camera view

from breadboardbot.display import *
from breadboardbot.face import *
from breadboardbot.platform_esp32s3 import *
from breadboardbot.http_controller import *
import mdns
import wifi
import wifi_config

# Connect to wifi
wifi.radio.connect(wifi_config.SSID, wifi_config.PASSWORD)
mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = "esp32s3"
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=80)

bot = Robot(i2c=True, camera=True, server=True)
face = Face()
face.say(str(wifi.radio.ipv4_address))

@bot.server.route("/")
def home(request: Request):
    return FileResponse(request, "basic_http_control_with_cam.html", "/www")

@bot.server.route("/cam.jpg")
def cam(request: Request):
    return Response(request, bot.cam.take(0.5), content_type="image/jpeg")

def handle_httpcommand(request):
    if request.path == "/forward":
        bot.drive(1, 1)
    elif request.path == "/backward":
        bot.drive(-1, -1)
    elif request.path == "/left":
        bot.drive(-1, 1)
    elif request.path == "/right":
        bot.drive(1, -1)
    elif request.path == "/stop":
        bot.drive(0, 0)
    return "OK"

bot.loop_forever(
    behaviors=[
        DisplayBehavior(bot.i2c, face),
        BasicHTTPListener(bot.server, handle_httpcommand),
    ]
)
