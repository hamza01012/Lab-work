import json
import requests
import paho.mqtt.client as mqtt

# === ThingSpeak Config ===
THINGSPEAK_API_KEY = "D4RU97CF0LEOXL7Q"
THINGSPEAK_URL = "https://api.thingspeak.com/update"

# === MQTT Config ===
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "agri/sensor/data"

# === MQTT Callback ===
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        print("📥 Received:", payload)

        # Prepare ThingSpeak fields
        data = {
            "api_key": THINGSPEAK_API_KEY,
            "field1": payload.get("temperature"),
            "field2": payload.get("humidity"),
            "field3": payload.get("mq135_ao"),
            "field4": payload.get("mq135_do"),
            "field5": payload.get("ldr_ao"),
            "field6": payload.get("ldr_do"),
            "field7": payload.get("soil_ao"),
            "field8": payload.get("soil_do")
        }

        response = requests.post(THINGSPEAK_URL, data=data)
        print("📤 Sent to ThingSpeak:", response.text)

    except Exception as e:
        print("❌ Error:", e)

# === MQTT Setup ===
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.subscribe(MQTT_TOPIC)

print("🚀 Forwarding MQTT to ThingSpeak...")
client.loop_forever()
