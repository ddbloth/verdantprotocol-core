
import pytest
from automation.rules import evaluate_rules

def test_evaluate_rules_no_data(caplog):
    evaluate_rules({})
    assert "No sensor data to evaluate." in caplog.text

def test_evaluate_rules_no_rules(caplog):
    data = {
        "node_id": "node01",
        "sensor_type": "light",
        "value": 1000,
        "unit": "lux",
        "timestamp": "2025-10-03T15:00:00Z"
    }
    evaluate_rules(data)
    assert "No rules defined for sensor type: light" in caplog.text

def test_evaluate_rules_trigger_max(caplog):
    data = {
        "node_id": "node01",
        "sensor_type": "temperature",
        "value": 90.0,
        "unit": "C",
        "timestamp": "2025-10-03T15:00:00Z"
    }
    evaluate_rules(data)
    assert "Rule triggered for temperature: decrease" in caplog.text

def test_evaluate_rules_trigger_min(caplog):
    data = {
        "node_id": "node01",
        "sensor_type": "humidity",
        "value": 30.0,
        "unit": "%",
        "timestamp": "2025-10-03T15:00:00Z"
    }
    evaluate_rules(data)
    assert "Rule triggered for humidity: increase" in caplog.text