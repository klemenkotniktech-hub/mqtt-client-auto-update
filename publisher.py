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
import smtplib
from email.message import EmailMessage
from pathlib import Path
from version import VERSION

load_dotenv()

def send_email(subject, body):
    message = EmailMessage()
    message["From"] = os.getenv("EMAIL_SENDER")
    message["To"] = os.getenv("EMAIL_RECIPIENT")
    message["Subject"] = subject
    message.set_content(body)

    with smtplib.SMTP(os.getenv("SMTP_SERVER"), int(os.getenv("SMTP_PORT"))) as server:
        server.starttls()
        server.login(
            os.getenv("EMAIL_SENDER"),
            os.getenv("EMAIL_PASSWORD")
        )
        server.send_message(message)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

BROKER = "localhost"
PORT = 8885
TOPIC = "sensor/environment"

DEVICE_ID = "senzor_01"

UPDATE_MARKER = Path("update_completed")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.tls_set(
    ca_certs="certs/ca.crt",
    tls_version=ssl.PROTOCOL_TLS_CLIENT
)
client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)


client.connect(BROKER, PORT)

# pošiljanje maila po update-u
if UPDATE_MARKER.exists():
    try:
        send_email(
            "MQTT client update completed",
            f"MQTT client version {VERSION} was successfully updated."
        )
    except Exception as e:
        print(f"Failed to send update completion email: {e}")

    UPDATE_MARKER.unlink()



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
        try:
            send_email(
                "MQTT client update started",
                f"Updating MQTT client from version {VERSION} to {update}."
            )
        except Exception as e:
            print(f"Failed to send email: {e}")

        print("Update available. Exiting application.")
        sys.exit(0)


    time.sleep(5)
