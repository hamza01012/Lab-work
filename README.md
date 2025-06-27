# 🌱 Environmental Classification for Plants (IoT + ML Project)

An IoT-based environmental monitoring system using ESP32, sensors, MQTT, and machine learning to classify environmental conditions critical for healthy plant growth. Data is logged locally in InfluxDB and visualized on the cloud via ThingSpeak.

---

## 📌 Project Overview

This project combines real-time sensor readings with a trained machine learning model to classify the environment into one of the following categories:

- ✅ Optimal
- 🌿 Moist
- 🔥 Dry
- 💧 Wet
- 🌫 LowLight
- 🏭 HighPollution

Sensor readings are collected using an ESP32-S3 board and published via MQTT. A Python backend listens to the MQTT topic, predicts the environment using a trained Random Forest model, and sends the data to InfluxDB and ThingSpeak.

---

## 🔧 Tech Stack

- **ESP32-S3** (Arduino IDE)  
- **Sensors:** DHT11, MQ135, LDR, Soil Moisture (AO + DO)  
- **MQTT Broker:** Mosquitto  
- **Machine Learning:** RandomForestClassifier (scikit-learn)  
- **Data Logging:** InfluxDB, ThingSpeak  
- **Language:** Python (for backend)

---

## 📡 Sensor Data Features

| Sensor           | Field Name    |
|------------------|---------------|
| Temperature       | `temperature` |
| Humidity          | `humidity`    |
| Air Quality (AO)  | `mq135_ao`    |
| Light (AO)        | `ldr_ao`      |
| Soil Moisture (AO)| `soil_ao`     |

⚠️ Digital outputs are collected but not used in model training.

---

## 🧠 Model Training

- Input Features: `temperature`, `humidity`, `mq135_ao`, `ldr_ao`, `soil_ao`
- Classes: `Optimal`, `Dry`, `Moist`, `Wet`, `LowLight`, `HighPollution`
- Trained using `RandomForestClassifier` on a labeled synthetic dataset
- Model saved as: `environment_model.pkl`
- Label encoder saved as: `label_encoder.pkl`

---

## 🌐 Cloud Visualization

- **InfluxDB:** Stores full sensor + predicted data locally
- **ThingSpeak:** Sends up to 8 fields for live monitoring (15s update limit)

---

## 🚀 How to Run

### 🧩 Requirements

```bash
pip install paho-mqtt influxdb-client joblib scikit-learn numpy
