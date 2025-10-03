# sensors/parser.py

import logging
import json

logger = logging.getLogger(__name__)

# Supported units and their normalization rules
UNIT_NORMALIZATION = {
    "C": "C",  # Celsius
    "F": "C",  # Fahrenheit → Celsius
    "°C": "C",
    "°F": "C",
    "percent": "%",
    "%": "%",
    "Pa": "Pa",
    "hPa": "Pa",
    "lux": "lux"
}

def normalize_unit(value, unit):
    """
    Normalize units to standard format and convert values if needed.
    Currently supports temperature (F → C), humidity (%), pressure (hPa → Pa).
    """
    try:
        unit = unit.strip()
        if unit in ["F", "°F"]:
            # Convert Fahrenheit to Celsius
            return round((value - 32) * 5.0 / 9.0, 2), "C"
        elif unit in ["hPa"]:
            # Convert hPa to Pa
            return round(value * 100), "Pa"
        elif unit in UNIT_NORMALIZATION:
            return value, UNIT_NORMALIZATION[unit]
        else:
            logger.warning(f"Unknown unit '{unit}', passing through unmodified.")
            return value, unit
    except Exception as e:
        logger.error(f"Error normalizing unit '{unit}': {e}")
        return value, unit  # Fallback to original

def parse_sensor_data(topic: str, payload: str) -> dict:
    """
    Parses MQTT topic and payload from a sensor node.

    Expected topic format:
        verdant/sensors/{node_id}/{sensor_type}

    Expected payload format:
        JSON string with sensor reading, e.g.:
        {
            "value": 23.5,
            "unit": "C",
            "timestamp": "2025-10-03T14:55:00Z"
        }

    Returns:
        dict with parsed and normalized data:
        {
            "node_id": "node01",
            "sensor_type": "temperature",
            "value": 23.5,
            "unit": "C",
            "timestamp": "2025-10-03T14:55:00Z"
        }
    """
    try:
        # Validate and parse topic
        parts = topic.strip().split('/')
        if len(parts) != 4 or parts[0] != "verdant" or parts[1] != "sensors":
            logger.warning(f"Unexpected topic format: {topic}")
            return {}

        node_id = parts[2]
        sensor_type = parts[3]

        # Parse JSON payload
        data = json.loads(payload)

        # Validate expected keys
        required_keys = {"value", "unit", "timestamp"}
        if not required_keys.issubset(data.keys()):
            logger.warning(f"Incomplete payload data: {payload}")
            return {}

        # Normalize unit and value
        normalized_value, normalized_unit = normalize_unit(data["value"], data["unit"])

        return {
            "node_id": node_id,
            "sensor_type": sensor_type,
            "value": normalized_value,
            "unit": normalized_unit,
            "timestamp": data["timestamp"]
        }

    except json.JSONDecodeError:
        logger.error(f"Failed to decode JSON payload: {payload}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error parsing sensor data: {e}")
        return {}could you 