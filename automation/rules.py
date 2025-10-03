# automation/rules.py

import logging
import json
import paho.mqtt.client as mqtt
from mqtt.topics import get_control_topic
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)

# MQTT control topic base
CONTROL_TOPIC_BASE = "verdant/control"

# TODO: Move thresholds to config file or database
THRESHOLDS = {
    "temperature": {
        "max": 85.0,  # °F
        "min": 60.0
    },
    "humidity": {
        "max": 80.0,  # %
        "min": 40.0
    },
    "soil_moisture": {
        "min": 30.0  # %
    }
}

# Create a lightweight MQTT client for publishing control commands
mqtt_client = mqtt.Client()
mqtt_client.connect("localhost", 1883)  # TODO: Use .env config

def evaluate_rules(sensor_data: dict):
    """
    Evaluates sensor data against predefined thresholds.
    If a rule is triggered, publishes a control command.

    Args:
        sensor_data (dict): Parsed sensor data from parser.py
    """
    if not sensor_data:
        logger.warning("No sensor data to evaluate.")
        return

    node_id = sensor_data["node_id"]
    sensor_type = sensor_data["sensor_type"]
    value = sensor_data["value"]

    logger.info(f"Evaluating {sensor_type} from {node_id}: {value}")

    # Check if we have rules for this sensor type
    if sensor_type not in THRESHOLDS:
        logger.info(f"No rules defined for sensor type: {sensor_type}")
        return

    thresholds = THRESHOLDS[sensor_type]

    # Determine if action is needed
    action = None
    if "max" in thresholds and value > thresholds["max"]:
        action = "decrease"
    elif "min" in thresholds and value < thresholds["min"]:
        action = "increase"

    if action:
        logger.info(f"Rule triggered for {sensor_type}: {action}")
        send_control_command(node_id, sensor_type, action)
    else:
        logger.info(f"{sensor_type} value within acceptable range.")


def send_control_command(node_id: str, sensor_type: str, action: str):
    """
    Publishes a control command to the actuator topic.
    """
    topic = get_control_topic(node_id, sensor_type)
    timestamp = datetime.utcnow().isoformat() + "Z"

    payload = json.dumps({
        "action": action,
        "source": "master",
        "timestamp": timestamp
    })

    mqtt_client.publish(topic, payload)
    logger.info(f"Published control command to {topic}: {payload}")