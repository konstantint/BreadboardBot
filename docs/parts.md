# Parts and tools

To build the BreadboardBot you will need to obtain the following parts and tools.

## Body

| **Image**&nbsp;&nbsp; | **Component** | **Price** | **Notes** |
| --------------------- | ------------- | --------- | --------- |
| <img src="img/part-xiao-rp2040.jpg" width="50"> | [Xiao RP2040](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html) | $6 | The Seeedstudio Xiao series includes several microcontrollers with the same, pin-compatible form-factor. Moreover, there are pin-compatible boards from other vendors ([example](https://www.adafruit.com/product/5426)). Most of those could be used as a drop-in replacement to the Xiao RP2040 in the BreadboardBot (with appropriate update to the code and, maybe, some wiring changes). This is one of the things that makes the BreadboardBot exciting (e.g. [Xiao ESP32S3 Sense](https://www.seeedstudio.com/XIAO-ESP32S3-Sense-p-5639.html) is a pin-compatible microcontroller with Wifi, Bluetooth, microphone and camera).<br>Pin compatibility with the Xiao is not a strict requirement either. For example you can build a [line-follower BreadboardBot](examples/m5atom_line_follower.md) or a Bluetooth-joystick-steerable Breadboardbot with the [M5Stack Atom](https://shop.m5stack.com/products/atom-lite-esp32-development-kit).<br>The Xiao RP2040, however, is the current "recommended starter model" for making a BreadboardBot. It is cheap (do get a few replacements to break), beginner-friendly (due to CircuitPython support) and quite tolerant to some of the sloppy electrical connections used in the bot.<br>In any case *do not* get the Xiao SAMD21 (which may be tempting as it is sold with presoldered headers). This model seems to operate the motors incorrectly when powered by the 4.5V battery of the BreadboardBot. It also has way uncomfortably little space for storing your scripts.<br>As I try BreadboardBot with other MCUs more examples will appear here.|
| <img src="img/part-breadboard.jpg" width="50"> | [Mini-breadboard](https://aliexpress.com/item/1005006054688190.html) | $0.5 |  |
| <img src="img/part-servo.jpg" width="50"> | 2 x [FS90R continuous servo + wheel](https://aliexpress.com/item/33046263381.html) | $6 | The version with lego-style wheels is the most convenient (as you can easily take them off and put back on). Note that the linked servos are not the most reliable and you might want to get a backup or two. |
| <img src="img/part-servo-2.jpg" width="50"> | **or** 2 x [Geekservo continuous servo + wheel](http://aliexpress.com/item/1005004296651771.html) | $12 | Alternatively, you can get these "GeekServo" motors with LEGO-style axes. They cost more, but are more colorful and seem slightly more precise and reliable. Note that they are slower than the FS90R servos above. |
| <img src="img/part-batterybox.jpg" width="50"> | [3xAAA battery box](https://aliexpress.com/item/1005003772254191.html) | $1 | Make sure you get the one with an on-off switch. <br>Note that the choice of a 3xAAA box assumes you plan to use **non-rechargeable** (1.5V) batteries. In this case the box will produce ~4.5V of voltage when the batteries are charged. This is actually somewhat suboptimal as it is already below the ideal 5V and will fall even lower as the batteries gradually discharge. As the voltage reaches 4.0-4.3V (the actual threshold depends on the microcontroller model), your robot might start to behave strangely or stop working at first partially and then completely way before the full resource of the batteries is exhausted (e.g. Wifi or Bluetooth on the ESP32 MCUs seem to become very unreliable at voltages below 4.3 already). A perhaps slightly better option is to use a 4xAAA box with four **NiMH rechargeable (1.3V)** batteries. If you already have rechargeables at home, do get that one, but **do not** power the robot from four non-rechargeable batteries, as the resulting 6V will be above the supported supply voltage for all the MCUs listed in these instructions.<br>(Another option would be to add a small boost converter to the breadboard, but it is currently not documented here - feel free to experiment with it if you are looking for something to try). |
| <img src="img/part-casterball.jpg" width="50"> | [Self-adhesive caster ball](https://aliexpress.com/item/1005005159921275.html) | $0.4 | The caster ball is optional. I've yet to find one with the appearance that I like. |

NB: AliExpress links here point to somewhat arbitrarily chosen sellers that I personally used to order the parts. They might become stale or you might be able to find the same components cheaper (for the particular quantity you need) elsewhere. The prices match what I paid when ordering components for 5 kits, including shipping.

## Sensors / actuators

You can plug a variety of breadboard-friendly gadgets into the robot, as long as they don't have too many pins and work with 3.3V power.

The components listed below are just a small selection of things that have been tested so far and are supported by some of the provided code examples.

| **Image**&nbsp;&nbsp; | **Component** | **Price** | **Notes** | **Example** |
| --------------------- | ------------- | --------- | --------- | -- |
| <img src="img/part-linesensor.jpg" width="50"> | 2 x [Line-tracker sensor](https://aliexpress.com/item/1005003297744025.html)  | $1 | Make sure you get the model with pins ordered OUT, VCC, GND (when the sensor is looking down). | [[1](examples/line_follower.md)] 
| <img src="img/part-rcwl1601.jpg" width="50"> | [RCWL-1601 sonar](https://aliexpress.com/item/1005004215620216.html)  | $1.5 | NB: This is *not* the popular HC-SR04 ("blue") sensor. The blue one requires 5V input, this one works with 3.3V. | [[1](examples/line_follower_sonar.md)] 
| <img src="img/part-buzzer.jpg" width="50"> | [Passive buzzer](https://aliexpress.com/item/1005006205295709.html)  | $0.2 | There are many options, I've yet to find one that fits the breadboard perfectly. | [[1](examples/line_follower_sonar_button_buzzer.md)] 
| <img src="img/part-button-1.jpg" width="50"> | Button ([1](https://de.aliexpress.com/item/32834276752.html), [2](https://aliexpress.com/item/32843612610.html))  | $0.05 | There are many options, I've yet to find one that I like best. | [[1](examples/line_follower_sonar_button_buzzer.md)] 
| <img src="img/part-screen.jpg" width="50"> | [0.96" SSD1306 OLED](https://aliexpress.com/item/1005005281256695.html)  | $2 | | [[1](examples/line_follower_oled.md)] 
| <img src="img/part-hc06.jpg" width="50"> | [HC06 Bluetooth serial transceiver (4-pin)](https://aliexpress.com/item/1005005648270683.html)  | $2.4 | | [[1](examples/oled_bluetooth.md)] 
| <img src="img/part-dht11.jpg" width="50"> | [DHT11 humidity & temperature sensor](https://aliexpress.com/item/1005006223904588.html)  | $0.7 | | [[1](examples/oled_oled_dht11.md)] 
| <img src="img/part-ds3231.jpg" width="50"> | [DS3231 real-time clock](https://de.aliexpress.com/item/1005006359914113.html)  | $1.6 | | [[1](examples/oled_oled_ds3231.md)] 
| <img src="img/part-ir.jpg" width="50"> | [IR proximity sensor](https://de.aliexpress.com/item/1005005064947064.html)  | $1 | | [[1](examples/oled_oled_ir.md)] 
| <img src="img/part-xiao-rgb-matrix.jpg" width="50"> | [Xiao 6x10 RGB Matrix](https://www.seeedstudio.com/6x10-RGB-MATRIX-for-XIAO-p-5771.html)  | $5 | Get two of them if you have the budget. You will also need 17mm pin headers to attach the matrix suspended above the main microcontroller. | [[1](examples/xiao_rgb_matrix.md)]

## Expendables

You will need some expendable materials to assemble the robot as well as a set of breadboard wires.

| **Image**&nbsp;&nbsp; | **Component** | **Notes** |
| --------------------- | ------------- | --------- |
| <img src="img/part-wires.jpg" width="50">  | [Breadboard jumper wire set](https://aliexpress.com/item/1005004530477894.html) |  You will only need 10 or so from the set, but you might find use for others later anyway.
| <img src="img/part-bolts.jpg" width="50">  | 2 x [M2 bolts](https://aliexpress.com/item/32907505613.html) 5-8mm | The bolts are somewhat optional - you can just stick the motors on the back of the breadboard without them. However, adding the screws makes the construction much more durable. The required length of the bolts depends on whether the head will sink inside the opening.
|   | Hot glue | In theory this can be any glue that will stick servo connectors to the side of the breadboard. I was hoping superglue would work, but it somewhy did not hold at all for me. Hot glue did the job very well. This may depend on the actual plastic used for the breadboard - it seems there are slight variations.
|  | [Two-sided sticky tape](https://aliexpress.com/item/1005005380522382.html) | Any two-sided tape should do, but I really like the linked one (the 30mm-wide one). Worth having at home in general.
| <img src="img/part-pinheader.jpg" width="50">   | [Pin headers](https://aliexpress.com/item/1005003012878518.html) | Firstly, you will definitely need the "usual", male, 11mm headers (2 sets of 7 pins) to solder onto the MCU. In addition, headers for the battery box are needed and there are two options. The "basic" one is to solder two 11mm male pin headers to the battery wires (in this case you might also want to get some heatshrink or insulation wire). A fancier option (less prone to a battery misconnection that can burn your MCU) is to crimp a 3x1 *female* header on the battery wire (you will need a crimper tool for that) and have it plug onto male headers sticking out of the breadboard. For that you will need to get three 15mm male pin headers. Finally, if you want to attach the RGB matrix, get a row of 17mm male pin headers as well.

## Tools

You will need scissors to cut the sticky tape, a screwdriver for screwing the bolts, a hot glue gun (unless you find a different glue for fixing servo connectors on the breadboard) and a soldering iron to solder pinheaders to the MCU. The two additional (optional and perhaps less common) tools that I personally ended up using are:

| **Image**&nbsp;&nbsp; | **Component** | **Notes** |
| --------------------- | ------------- | --------- |
|  <img src="img/tool-drill.jpg" width="50">   | [Hand twist drill](https://aliexpress.com/item/1005005264022948.html) | A small hand-twist drill (which you can get for $3 sometimes) can be quite useful for making the 2mm holes in the servos which you need to then bolt them to the breadboard. You might find different ways of getting those holes or, as mentioned above, simply avoid bolting the motors to the breadboard completely.
| <img src="img/tool-crimper.jpg" width="50">  | [Dupont wire crimper tool](https://aliexpress.com/item/1005005699142549.html) | This is optional and only needed if you want to make a "fancier" battery connector.

## Extras

The absolutely optional but incredibly convenient extra is:

| **Image**&nbsp;&nbsp; | **Component** | **Notes** |
| --------------------- | ------------- | --------- |
|  <img src="img/part-usbcable.jpg" width="50">   | [Magnetic, 90-degree twistable USB cable](https://aliexpress.com/item/1005004971580228.html) | Allows you to easily connect to the microcontroller on the breadboard without having to remove the wheels every time.

Once you've gotten all the parts, proceed to [assemble them](assembly.md).