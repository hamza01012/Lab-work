from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import network
import socket
import dht
import neopixel

# Wi-Fi configuration (Access Point mode)
AP_SSID = "ESP32-S3_AP"
AP_PASSWORD = "12345678"

# OLED size
WIDTH = 128
HEIGHT = 64

# I2C setup (using GPIO 9 for SDA and 8 for SCL)
i2c = I2C(0, scl=Pin(9), sda=Pin(8))

# Initialize OLED
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.text('Starting AP...', 0, 0)
oled.show()

# Set up ESP32 in AP mode
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

print('Starting Access Point...')
while not ap.active():
    pass

print('AP Started. IP:', ap.ifconfig()[0])
oled.fill(0)
oled.text('AP Mode Active', 0, 0)
oled.text(f'IP: {ap.ifconfig()[0]}', 0, 10)
oled.show()

# DHT11 sensor setup (GPIO 4)
dht_sensor = dht.DHT11(Pin(4))

# Neopixel setup for RGB LED (GPIO 48)
np = neopixel.NeoPixel(Pin(48), 1)

# HTML Page
html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 Sensor & LED Control</title>
    <style>
        /* General styling */
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: linear-gradient(135deg, #63116b, #2575fc);
            color: white;
            padding: 20px;
        }

        h1 {
            font-size: 2.5em;
        }

        .description {
            font-size: 1.2em;
            max-width: 700px;
            margin: 0 auto 30px;
            line-height: 1.6;
        }

        /* Container and box styling */
        .top {
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 20px;
        }

        .container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 20px;
            max-width: 1000px;
            margin: 0 auto;
        }

        .box {
            flex: 1;
            min-width: 300px;
            padding: 30px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        }

        h2 {
            font-size: 1.8em;
            margin-bottom: 20px;
        }

        p {
            font-size: 1.2em;
            margin-bottom: 15px;
        }

        /* Sliders */
        input[type=range] {
            -webkit-appearance: none;
            appearance: none;
            width: 100%;
            height: 12px;
            border-radius: 6px;
            outline: none;
            margin-bottom: 20px;
        }

        input[type=range]::-webkit-slider-thumb {
            -webkit-appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: white;
            cursor: pointer;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
        }

        /* Slider backgrounds */
        #red { background: linear-gradient(to right, #000, red); }
        #green { background: linear-gradient(to right, #000, green); }
        #blue { background: linear-gradient(to right, #000, blue); }

        /* Buttons */
        button {
            padding: 12px 25px;
            font-size: 1em;
            background-color: #00d4ff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }

        button:hover {
            background-color: #00a1cc;
        }

        /* Text input */
        input[type=text] {
            width: calc(100% - 20px);
            padding: 10px;
            border: none;
            border-radius: 6px;
            font-size: 1em;
            margin-bottom: 20px;
        }
    </style>
</head>

<body>
    <!-- Main Heading -->
    <h1>ESP32-S3 Sensor & LED Control</h1>

    <!-- Short Description -->
    <p class="description">
        This web interface allows you to interact with your ESP32-S3. Monitor real-time sensor data from the DHT11, control the RGB LED’s color, and display messages on the OLED screen.
    </p>

    <div class="top">
        <div class="container">
            <!-- Sensor Readings -->
            <div class="box">
                <h2>🌡 Sensor Readings</h2>
                <p>Temperature: <span id="temp">--</span> °C</p>
                <p>Humidity: <span id="hum">--</span> %</p>
            </div>

            <!-- RGB LED Control -->
            <div class="box">
                <h2>🎨 RGB LED Control</h2>
                <label for="red">Red</label>
                <input type="range" id="red" min="0" max="255">

                <label for="green">Green</label>
                <input type="range" id="green" min="0" max="255">

                <label for="blue">Blue</label>
                <input type="range" id="blue" min="0" max="255">

                <button onclick="updateColor()">Set Color</button>
            </div>

            <!-- OLED Display Control -->
            <div class="box">
                <h2>📺 OLED Display</h2>
                <input type="text" id="message" placeholder="Enter your message">
                <button onclick="sendMessage()">Send Message</button>
            </div>
        </div>
    </div>

    <script>
        // Fetch sensor data every 2 seconds
        setInterval(function() {
            fetch('/sensor')
                .then(response => response.json())
                .then(data => {
                    document.getElementById('temp').textContent = data.temperature;
                    document.getElementById('hum').textContent = data.humidity;
                })
                .catch(error => console.error('Error fetching sensor data:', error));
        }, 2000);

        // Send RGB values to ESP32
        function updateColor() {
            const red = document.getElementById('red').value;
            const green = document.getElementById('green').value;
            const blue = document.getElementById('blue').value;

            fetch(`/color?red=${red}&green=${green}&blue=${blue}`)
                .then(response => console.log('RGB values sent:', { red, green, blue }))
                .catch(error => console.error('Error sending RGB values:', error));
        }

        // Send message to OLED
        function sendMessage() {
            const message = document.getElementById('message').value;
            fetch(`/message?text=${encodeURIComponent(message)}`)
                .then(response => console.log('Message sent:', message))
                .catch(error => console.error('Error sending message:', error));
        }
    </script>
</body>
</html>

"""

# Web server
def web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(5)
    print('Web server running...')

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')

        if '/sensor' in request:
            try:
                dht_sensor.measure()
                temp = dht_sensor.temperature()
                hum = dht_sensor.humidity()
                response = '{{"temperature": {}, "humidity": {}}}'.format(temp, hum)
            except:
                response = '{"temperature": "Error", "humidity": "Error"}'
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + response)

        elif '/color' in request:
            try:
                red = int(request.split('red=')[1].split('&')[0])
                green = int(request.split('green=')[1].split('&')[0])
                blue = int(request.split('blue=')[1].split(' ')[0])
                np[0] = (red, green, blue)
                np.write()
            except:
                pass
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nColor updated')

        elif '/message' in request:
            message = request.split('text=')[1].split(' ')[0].replace('+', ' ')
            oled.fill(0)
            oled.text(message, 0, 20)
            oled.show()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nMessage displayed')

        else:
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)

        conn.close()

web_server()