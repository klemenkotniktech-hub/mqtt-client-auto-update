import paho.mqtt.client as mqtt
import json
import random
from datetime import datetime
import time
import ssl
import os
from dotenv import load_dotenv
from update import check_for_update
import sys

load_dotenv()

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

BROKER = "localhost"
PORT = 8885
TOPIC = "sensor/environment"

DEVICE_ID = "senzor_01"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(
    ca_certs="certs/ca.crt",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


client.connect(BROKER, PORT)


while True:
    data = {
        "device_id" : DEVICE_ID,
        "timestamp": datetime.now().replace(microsecond=0).isoformat(),
        "temperature": round(random.uniform(20, 30), 2),
        "humidity": round(random.uniform(40, 60), 2),
        "pressure": round(random.uniform(990, 1030), 2),
    }
    payload = json.dumps(data)

    client.publish(TOPIC, payload)

    print(f"Published payload: {payload}")

    # check for update
    update = check_for_update()
    if update:
        print("Update available. Exiting application.")
        sys.exit(0)


    time.sleep(5)
