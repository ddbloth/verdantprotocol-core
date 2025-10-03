# mqtt/client.py

import paho.mqtt.client as mqtt
from mqtt.topics import parse_sensor_topic
import logging
from sensors.parser import parse_sensor_data
from automation.rules import evaluate_rules

# MQTT Broker Configuration
BROKER_ADDRESS = "localhost"  # TODO: Move to .env for flexibility
BROKER_PORT = 1883
TOPIC_SUBSCRIBE = "verdant/sensors/#"

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# MQTT Event Handlers
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT Broker successfully.")
        client.subscribe(TOPIC_SUBSCRIBE)
        logger.info(f"Subscribed to topic: {TOPIC_SUBSCRIBE}")
    else:
        logger.error(f"Failed to connect, return code {rc}")

# Helper function to parse topic into metadata
def on_message(client, userdata, msg):
    logger.info(f"Received message on {msg.topic}: {msg.payload.decode()}")

    # Parse topic into metadata
    topic_info = parse_sensor_topic(msg.topic)
    if not topic_info:
        logger.warning("Invalid sensor topic format.")
        return

    # Parse payload
    sensor_data = parse_sensor_data(msg.topic, msg.payload.decode())

    # Merge topic info into sensor_data if needed
    sensor_data.update(topic_info)

    # Evaluate rules
    evaluate_rules(sensor_data)

def create_mqtt_client():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    # TODO: Add authentication if needed
    # client.username_pw_set("user", "password")

    client.connect(BROKER_ADDRESS, BROKER_PORT, keepalive=60)
    return client