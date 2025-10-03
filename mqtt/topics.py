# mqtt/topics.py

# Base topic prefixes
SENSOR_BASE = "verdant/sensors"
CONTROL_BASE = "verdant/control"

def get_sensor_topic(node_id: str, sensor_type: str) -> str:
    """
    Constructs a topic for publishing sensor data.
    Example: verdant/sensors/node01/temperature
    """
    return f"{SENSOR_BASE}/{node_id}/{sensor_type}"

def get_control_topic(node_id: str, actuator_type: str) -> str:
    """
    Constructs a topic for sending control commands.
    Example: verdant/control/node01/fan
    """
    return f"{CONTROL_BASE}/{node_id}/{actuator_type}"

def parse_sensor_topic(topic: str) -> dict:
    """
    Parses a sensor topic into components.
    Returns: { 'node_id': ..., 'sensor_type': ... }
    """
    parts = topic.split('/')
    if len(parts) == 4 and parts[0] == "verdant" and parts[1] == "sensors":
        return {
            "node_id": parts[2],
            "sensor_type": parts[3]
        }
    return {}

def parse_control_topic(topic: str) -> dict:
    """
    Parses a control topic into components.
    Returns: { 'node_id': ..., 'actuator_type': ... }
    """
    parts = topic.split('/')
    if len(parts) == 4 and parts[0] == "verdant" and parts[1] == "control":
        return {
            "node_id": parts[2],
            "actuator_type": parts[3]
        }
    return {}
