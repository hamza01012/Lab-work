import json
import numpy as np
import paho.mqtt.client as mqtt
import joblib
from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS




# Load model and encoder
model = joblib.load("environment_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# InfluxDB Configuration (replace with your actual values)
INFLUXDB_URL = "http://localhost:8086"
INFLUXDB_TOKEN = "9CQjBpLBmWJXpjzJ6iDBwfKMRWqw9UN9kSGNrD-a8sd-0RTnkJvhjdy0REftMuc1UP_kXFSXCcdwOsDAKztarQ=="
INFLUXDB_ORG = "my-org"
INFLUXDB_BUCKET = "environmental_classification_project"

client_influx = InfluxDBClient(
    url=INFLUXDB_URL,
    token=INFLUXDB_TOKEN,
    org=INFLUXDB_ORG,
)

write_api = client_influx.write_api(write_options=WriteOptions(batch_size=1))

# MQTT Configuration
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "agri/sensor/data"

# Format input for prediction
def prepare_input(sensor_json):
    return np.array([[ 
        sensor_json["temperature"],
        sensor_json["humidity"],
        sensor_json["mq135_ao"],
        sensor_json["ldr_ao"],
        sensor_json["soil_ao"]
    ]])

# Handle incoming MQTT messages
def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode())
        input_data = prepare_input(payload)
        prediction = model.predict(input_data)
        predicted_class = label_encoder.inverse_transform(prediction)[0]
        print("✅ Predicted:", predicted_class)

        # Write to InfluxDB
        point = (
            Point("environment")
            .tag("location", "test_field")
            .tag("predicted_class", predicted_class)  # ✅ change from field to tag
            .field("temperature", float(payload["temperature"]))
            .field("humidity", float(payload["humidity"]))
            .field("mq135_ao", int(payload["mq135_ao"]))
            .field("ldr_ao", int(payload["ldr_ao"]))
            .field("soil_ao", int(payload["soil_ao"]))
        )

        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)

    except Exception as e:
        print("❌ Error:", e)

# MQTT Setup
client_mqtt = mqtt.Client()
client_mqtt.on_message = on_message
client_mqtt.connect(MQTT_BROKER, MQTT_PORT, 60)
client_mqtt.subscribe(MQTT_TOPIC)

print("🚀 Waiting for sensor data...")
client_mqtt.loop_forever()
