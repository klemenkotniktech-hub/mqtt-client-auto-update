import json
import paho.mqtt.client as mqtt
from datetime import datetime
from database import save_sensor_data
import ssl
import os
from dotenv import load_dotenv
from version import VERSION

load_dotenv()

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")


BROKER = "localhost"
PORT = 8885
TOPIC = "sensor/environment"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected to MQTT with result code {reason_code}")

    client.subscribe(TOPIC)
    print(f"Subscribed to topic: {TOPIC}")

def on_message(client, userdata, msg):
    received_timestamp = datetime.now().replace(microsecond=0)

    try:
        data = json.loads(msg.payload.decode())

        measurement_timestamp = datetime.fromisoformat(data["timestamp"]) # converts MQTT string conversion to datime format

        print(f"Measurement timestamp: {measurement_timestamp}")
        print(f"Received timestamp:    {received_timestamp}")
        print(f"Device: {data['device_id']}")
        print(f"Temperature: {data['temperature']} °C")
        print(f"Humidity: {data['humidity']} %")
        print(f"Pressure: {data['pressure']} hPa")

        save_sensor_data(
            device_id=data["device_id"],
            measurement_timestamp=measurement_timestamp,
            received_timestamp=received_timestamp,
            temperature=data["temperature"],
            humidity=data["humidity"],
            pressure=data["pressure"],
        )


    except (json.JSONDecodeError, KeyError) as error:
        print(f"Invalid message: {error}")



print(f"MQTT client version: {VERSION}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(
    ca_certs="certs/ca.crt",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)

client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT)

client.loop_forever()