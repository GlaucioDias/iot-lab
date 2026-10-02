import json
import os
from datetime import datetime

import paho.mqtt.client as mqtt

from .database import SessionLocal
from .models import Telemetry


MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

MQTT_TOPIC = os.getenv(
    "MQTT_TOPIC",
    "iot/+/telemetry"
)


def on_connect(
    client,
    userdata,
    flags,
    reason_code,
    properties
):

    print(
        f"[MQTT] Backend conectado: "
        f"{reason_code}"
    )

    client.subscribe(
        MQTT_TOPIC,
        qos=1
    )

    print(
        f"[MQTT] subscribed: {MQTT_TOPIC}"
    )


def on_message(
    client,
    userdata,
    message
):

    try:

        payload = json.loads(
            message.payload.decode("utf-8")
        )

        print(
            f"[MQTT] recebido: "
            f"{message.topic} -> {payload}"
        )

        telemetry = Telemetry(
            device_id=payload["device_id"],
            timestamp=datetime.fromisoformat(
                payload["timestamp"]
            ),
            temperature_c=payload["temperature_c"],
            humidity_pct=payload["humidity_pct"]
        )

        db = SessionLocal()

        try:

            db.add(telemetry)
            db.commit()

        finally:

            db.close()

    except Exception as exc:

        print(
            f"[MQTT] erro processando mensagem: "
            f"{exc}"
        )


def start_mqtt():

    client = mqtt.Client(
        mqtt.CallbackAPIVersion.VERSION2,
        client_id="iot-backend"
    )

    client.username_pw_set(
        MQTT_USERNAME,
        MQTT_PASSWORD
    )

#   client.tls_set()

    client.on_connect = on_connect
    client.on_message = on_message

    print(
        f"[MQTT] conectando em "
        f"{MQTT_HOST}:{MQTT_PORT}"
    )

    client.connect(
        MQTT_HOST,
        MQTT_PORT,
        keepalive=60
    )

    client.loop_start()

    return client
