import json
import os
import random
import time
import uuid
from datetime import datetime, timezone

import paho.mqtt.client as mqtt


MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT", "8883"))
MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")

MQTT_TOPIC = os.getenv(
    "MQTT_TOPIC",
    "iot/+/telemetry"
)

DEVICE_ID = os.getenv(
    "SIMULATOR_DEVICE_ID",
    "esp32-001"
)

INTERVAL = float(
    os.getenv("SIMULATOR_INTERVAL", "2")
)


def on_connect(client, userdata, flags, reason_code, properties):
    print(f"[MQTT] conectado - reason_code={reason_code}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"[MQTT] desconectado - reason_code={reason_code}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"simulator-{DEVICE_ID}-{uuid.uuid4().hex[:8]}"
)

client.username_pw_set(
    MQTT_USERNAME,
    MQTT_PASSWORD
)

# HiveMQ Cloud utiliza TLS.
# client.tls_set()

client.on_connect = on_connect
client.on_disconnect = on_disconnect

# print(f"Conectando ao HiveMQ: {MQTT_HOST}:{MQTT_PORT}")

# client.connect(
#     MQTT_HOST,
#     MQTT_PORT,
#     keepalive=60
# )

while True:
    try:
        print(f"Conectando ao HiveMQ: {MQTT_HOST}:{MQTT_PORT}")

        client.connect(
            MQTT_HOST,
            MQTT_PORT,
            keepalive=60
        )

        break

    except Exception as e:
        print(f"MQTT indisponível: {e}")
        print("Tentando novamente em 5 segundos...")
        time.sleep(5)


client.loop_start()

while True:

    temperature = round(
        random.uniform(20.0, 32.0),
        2
    )

    humidity = round(
        random.uniform(40.0, 80.0),
        2
    )

    payload = {
        "device_id": DEVICE_ID,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),

        "temperature_c": temperature,
        "humidity_pct": humidity
    }

    topic = f"iot/{DEVICE_ID}/telemetry"

    result = client.publish(
        topic,
        json.dumps(payload),
        qos=1
    )

    print(
        f"[MQTT] {topic} -> {payload} "
        f"(result={result.rc})"
    )

    time.sleep(INTERVAL)
