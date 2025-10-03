# Pythong Utilities for Various Loths Lair Projects
# including the VerdantProtocol!

## 📝 Logger Module (`logger.py`)

The `logger.py` module provides a lightweight logging interface for recording sensor readings and actuator commands into a local SQLite database (`logs.db`). It is used throughout the VerdantProtocol system to persist environmental data and automation events.

### 📦 Features
- Initializes the database with two tables:
  - `sensor_readings`
  - `actuator_commands`
- Logs sensor data with timestamp, unit, and node ID
- Logs actuator commands with action, source, and timestamp
- Uses SQLite for local, portable storage

### 🚀 Usage

#### Initialize the Database

from utils.logger import initialize_database

initialize_database()


## Log a Sensor Reading
from utils.logger import log_sensor_reading

log_sensor_reading(
    node_id="node01",
    sensor_type="temperature",
    value=23.5,
    unit="C",
    timestamp="2025-10-03T15:00:00Z"
)

## Log an Actuator Command
from utils.logger import log_actuator_command

log_actuator_command(
    node_id="node01",
    actuator_type="fan",
    action="on",
    source="master"
)