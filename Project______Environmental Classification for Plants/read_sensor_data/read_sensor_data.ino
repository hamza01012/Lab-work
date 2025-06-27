#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

// ---------------- WiFi Credentials ----------------
const char* ssid = "Sajid Latif";           // Replace with your Wi-Fi SSID
const char* password = "SajidSahib4736#";   // Replace with your Wi-Fi password

// ---------------- Mosquitto MQTT Broker ----------------
const char* mqtt_server = "192.168.100.3";  // 🔁 Replace with your broker's IP (e.g., 192.168.1.10)
const int mqtt_port = 1883;
const char* mqtt_topic = "agri/sensor/data";

// ---------------- Sensor Pins ----------------
// DHT11
#define DHTPIN 4
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// MQ135
#define MQ135_AO 15
#define MQ135_DO 14

// LDR
#define LDR_AO 18
#define LDR_DO 12

// Soil Moisture
#define SOIL_AO 16
#define SOIL_DO 5

WiFiClient espClient;
PubSubClient client(espClient);

// ---------------- WiFi and MQTT Setup ----------------
void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to WiFi");
}

void connectToMQTT() {
  while (!client.connected()) {
    Serial.print("Connecting to MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      delay(2000);
    }
  }
}

// ---------------- Setup ----------------
void setup() {
  Serial.begin(115200);
  dht.begin();

  pinMode(MQ135_DO, INPUT);
  pinMode(LDR_DO, INPUT);
  pinMode(SOIL_DO, INPUT);

  connectToWiFi();
  client.setServer(mqtt_server, mqtt_port);
  connectToMQTT();
}

// ---------------- Main Loop ----------------
void loop() {
  if (!client.connected()) connectToMQTT();
  client.loop();

  // Sensor Readings
  float temp = dht.readTemperature();
  float humid = dht.readHumidity();

  int mq135_ao = analogRead(MQ135_AO);
  int mq135_do = digitalRead(MQ135_DO);

  int ldr_ao = analogRead(LDR_AO);
  int ldr_do = digitalRead(LDR_DO);

  int soil_ao = analogRead(SOIL_AO);
  int soil_do = digitalRead(SOIL_DO);

  // JSON Payload
  String payload = "{";
  payload += "\"temperature\":" + String(temp) + ",";
  payload += "\"humidity\":" + String(humid) + ",";
  payload += "\"mq135_ao\":" + String(mq135_ao) + ",";
  payload += "\"mq135_do\":" + String(mq135_do) + ",";
  payload += "\"ldr_ao\":" + String(ldr_ao) + ",";
  payload += "\"ldr_do\":" + String(ldr_do) + ",";
  payload += "\"soil_ao\":" + String(soil_ao) + ",";
  payload += "\"soil_do\":" + String(soil_do);
  payload += "}";

  // Publish
  Serial.println("Publishing: " + payload);
  client.publish(mqtt_topic, payload.c_str());

  delay(5000);  // Publish every 5 seconds
}
