import os
import sqlite3
import pytest
from utils.logger import initialize_database, log_sensor_reading, log_actuator_command

def test_initialize_database_creates_tables():
    initialize_database()
    conn = sqlite3.connect("data/logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    assert "sensor_readings" in tables
    assert "actuator_commands" in tables

def test_log_sensor_reading():
    log_sensor_reading("node01", "temperature", 22.5, "C", "2025-10-03T15:00:00Z")
    conn = sqlite3.connect("data/logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_readings WHERE node_id='node01'")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) > 0

def test_log_actuator_command():
    log_actuator_command("node01", "fan", "on", "master", "2025-10-03T15:00:00Z")
    conn = sqlite3.connect("data/logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actuator_commands WHERE node_id='node01'")
    rows = cursor.fetchall()
    conn.close()
    assert len(rows) > 0