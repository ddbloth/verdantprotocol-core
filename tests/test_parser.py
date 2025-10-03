
import pytest
from sensors.parser import parse_sensor_data

def test_valid_temperature_payload():
    topic = "verdant/sensors/node01/temperature"
    payload = '{"value": 90.0, "unit": "F", "timestamp": "2025-10-03T15:00:00Z"}'
    result = parse_sensor_data(topic, payload)
    assert result["node_id"] == "node01"
    assert result["sensor_type"] == "temperature"
    assert result["unit"] == "C"
    assert round(result["value"], 1) == 32.2  # 90°F → 32.2°C

def test_invalid_json_payload():
    topic = "verdant/sensors/node01/temperature"
    payload = 'not a json string'
    result = parse_sensor_data(topic, payload)
    assert result == {}