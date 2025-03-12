from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep
import network
import socket
import json

# OLED setup
WIDTH = 128
HEIGHT = 64
i2c = I2C(0, scl=Pin(9), sda=Pin(8))
oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.text('Starting AP...', 0, 0)
oled.show()

# AP mode setup
AP_SSID = "ESP32-S3_AP"
AP_PASSWORD = "12345678"
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=AP_SSID, password=AP_PASSWORD)

while not ap.active():
    pass

ip = ap.ifconfig()[0]
print('AP Started. IP:', ip)
oled.fill(0)
oled.text('AP Mode Active', 0, 0)
oled.text(f'IP: {ip}', 0, 10)
oled.show()

# HTML page with Wi-Fi connect form
html = """

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ESP32-S3 Control Panel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;500;700&display=swap">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Poppins', sans-serif;
            background: #0f172a;
            color: #f8fafc;
            text-align: center;
            padding: 30px;
        }
        h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 2rem;
            font-weight: 500;
            margin: 30px 0 15px;
        }
        button {
            padding: 12px 25px;
            font-size: 1.2rem;
            font-weight: 500;
            background: linear-gradient(135deg, #00d4ff, #0072ff);
            color: #fff;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        button:hover {
            transform: scale(1.05);
            background: linear-gradient(135deg, #0072ff, #00d4ff);
        }
        form {
            background: #1e293b;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
            max-width: 500px;
            margin: 0 auto;
        }
        label {
            display: block;
            font-size: 1.2rem;
            margin-bottom: 8px;
        }
        input, select {
            width: 100%;
            padding: 12px;
            font-size: 1.1rem;
            margin-bottom: 15px;
            border: none;
            border-radius: 8px;
            background: #334155;
            color: #f8fafc;
        }
        table {
            width: 100%;
            margin: 20px 0;
            border-collapse: collapse;
            background: #1e293b;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
        }
        th, td {
            padding: 15px;
            text-align: left;
            font-size: 1.1rem;
        }
        th {
            background: #00d4ff;
            color: #0f172a;
        }
        tr:nth-child(even) {
            background: #334155;
        }
        #status {
            font-size: 1.4rem;
            margin-top: 20px;
            font-weight: 500;
            color: #00d4ff;
        }
    </style>
</head>
<body>
    <h1>ESP32-S3 Control Panel</h1>

    <h2>Available Networks</h2>
    <button onclick="scanNetworks()">Scan Networks</button>
    <div id="networks"></div>

    <h2>Connect to Wi-Fi</h2>
    <form onsubmit="connectWiFi(event)">
        <label for="ssid">Select Network:</label>
        <select id="ssid" name="ssid" required></select>
        <br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required>
        <br>
        <button type="submit">Connect</button>
    </form>

    <div id="status"></div>

    <script>
        function scanNetworks() {
            fetch('/scan')
                .then(response => response.json())
                .then(data => {
                    let table = '<table><tr><th>SSID</th><th>RSSI</th><th>Security</th></tr>';
                    let options = '';
                    data.forEach(net => {
                        table += `<tr><td>${net.ssid}</td><td>${net.rssi} dBm</td><td>${net.security}</td></tr>`;
                        options += `<option value="${net.ssid}">${net.ssid}</option>`;
                    });
                    table += '</table>';
                    document.getElementById('networks').innerHTML = table;
                    document.getElementById('ssid').innerHTML = options;
                })
                .catch(error => console.error('Error scanning networks:', error));
        }

        function connectWiFi(event) {
            event.preventDefault();
            const ssid = document.getElementById('ssid').value;
            const password = document.getElementById('password').value;

            fetch('/connect', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ssid, password})
            })
            .then(response => response.text())
            .then(status => {
                document.getElementById('status').textContent = 'Status: ' + status;
            })
            .catch(error => console.error('Error connecting:', error));
        }
    </script>
</body>
</html>



"""

# Scan Wi-Fi networks
def scan_networks():
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    networks = sta.scan()
    sta.active(False)
    
    net_list = []
    for net in networks:
        ssid = net[0].decode('utf-8', 'ignore')
        rssi = net[3]
        auth = net[4]
        sec_type = "Open" if auth == 0 else "WPA/WPA2" if auth in [2, 3] else "WPA3"
        net_list.append({"ssid": ssid, "rssi": rssi, "security": sec_type})

    return json.dumps(net_list)

# Connect to Wi-Fi network
def connect_to_wifi(ssid, password):
    sta = network.WLAN(network.STA_IF)
    sta.active(True)
    sta.connect(ssid, password)
    
    timeout = 10
    while not sta.isconnected() and timeout > 0:
        sleep(1)
        timeout -= 1

    if sta.isconnected():
        ip = sta.ifconfig()[0]
        oled.fill(0)
        oled.text('Connected to:', 0, 0)
        oled.text(ssid, 0, 10)
        oled.text('IP: ' + ip, 0, 20)
        oled.show()
        return f'Connected! IP: {ip}'
    else:
        oled.fill(0)
        oled.text('Failed to connect', 0, 0)
        oled.show()
        return 'Connection Failed'

# Web server
def web_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('0.0.0.0', 80))
    s.listen(5)
    print('Web server running...')

    while True:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')

        if '/scan' in request:
            networks = scan_networks()
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n' + networks)

        elif '/connect' in request:
            data = json.loads(request.split('\r\n\r\n')[1])
            ssid = data.get('ssid')
            password = data.get('password')
            status = connect_to_wifi(ssid, password)
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n' + status)

        else:
            conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n' + html)

        conn.close()

web_server()