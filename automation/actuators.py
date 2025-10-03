# automation/actuators.py

import logging
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# MQTT Configuration
BROKER_ADDRESS = "localhost"  # TODO: Load from .env
BROKER_PORT = 1883
CONTROL_TOPIC_BASE = "verdant/control"

# Initialize MQTT client
mqtt_client = mqtt.Client()
mqtt_client.connect(BROKER_ADDRESS, BROKER_PORT)

def send_actuator_command(node_id: str, actuator_type: str, action: str):
    """
    Sends a control command to an actuator node via MQTT.

    Args:
        node_id (str): Target actuator node ID
        actuator_type (str): Type of actuator (e.g., "fan", "pump")
        action (str): Action to perform (e.g., "on", "off", "increase", "decrease")
    """
    topic = f"{CONTROL_TOPIC_BASE}/{node_id}/{actuator_type}"
    timestamp = datetime.utcnow().isoformat() + "Z"

    payload = json.dumps({
        "action": action,
        "source": "master",
        "timestamp": timestamp
    })

    mqtt_client.publish(topic, payload)
    logger.info(f"Sent actuator command to {topic}: {payload}")