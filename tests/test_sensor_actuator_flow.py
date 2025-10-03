# tests/test_sensor_actuator_flow.py

import time
import json
import paho.mqtt.client as mqtt

# Simulated sensor topic and payload
TEST_TOPIC = "verdant/sensors/node01/temperature"
TEST_PAYLOAD = json.dumps({
    "value": 90.0,  # Trigger threshold
    "unit": "F",
    "timestamp": "2025-10-03T15:00:00Z"
})

# MQTT Broker Configuration
BROKER_ADDRESS = "localhost"
BROKER_PORT = 1883

def on_message(client, userdata, msg):
    print(f"[TEST] Received message on {msg.topic}: {msg.payload.decode()}")

def run_test():
    print("[TEST] Starting sensor-actuator flow test...")

    # Create MQTT client
    client = mqtt.Client()
    client.on_message = on_message

    client.connect(BROKER_ADDRESS, BROKER_PORT)
    client.loop_start()

    # Subscribe to control topic to verify actuator command
    control_topic = "verdant/control/node01/temperature"
    client.subscribe(control_topic)

    # Publish simulated sensor data
    print(f"[TEST] Publishing sensor data to {TEST_TOPIC}")
    client.publish(TEST_TOPIC, TEST_PAYLOAD)

    # Wait to receive actuator command
    time.sleep(5)

    client.loop_stop()
    client.disconnect()
    print("[TEST] Test complete.")

if __name__ == "__main__":
    run_test()