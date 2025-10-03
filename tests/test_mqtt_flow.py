
import time
import json
import paho.mqtt.client as mqtt

BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883
TEST_TOPIC = "verdant/sensors/node01/temperature"
CONTROL_TOPIC = "verdant/control/node01/temperature"

def on_message(client, userdata, msg):
    print(f"[TEST] Received message on {msg.topic}: {msg.payload.decode()}")

def test_mqtt_sensor_to_actuator_flow():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.loop_start()
    client.subscribe(CONTROL_TOPIC)

    payload = json.dumps({
        "value": 90.0,
        "unit": "F",
        "timestamp": "2025-10-03T15:00:00Z"
    })
    client.publish(TEST_TOPIC, payload)

    time.sleep(5)
    client.loop_stop()
    client.disconnect()