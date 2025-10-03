import sqlite3
import logging
from datetime import datetime

# Setup logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Database file path
DB_PATH = "data/logs.db"  # Consider making this configurable via .env

def initialize_database():
    """
    Initializes the logs.db SQLite database with required tables.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Create sensor_readings table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sensor_readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                sensor_type TEXT NOT NULL,
                value REAL NOT NULL,
                unit TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        # Create actuator_commands table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS actuator_commands (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                node_id TEXT NOT NULL,
                actuator_type TEXT NOT NULL,
                action TEXT NOT NULL,
                source TEXT NOT NULL,
                timestamp TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")

def log_sensor_reading(node_id, sensor_type, value, unit, timestamp=None):
    """
    Inserts a new sensor reading into the sensor_readings table.
    """
    try:
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO sensor_readings (node_id, sensor_type, value, unit, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (node_id, sensor_type, value, unit, timestamp))
        conn.commit()
        conn.close()
        logger.info(f"Logged sensor reading: {node_id} {sensor_type} {value}{unit} at {timestamp}")
    except Exception as e:
        logger.error(f"Error logging sensor reading: {e}")

def log_actuator_command(node_id, actuator_type, action, source="master", timestamp=None):
    """
    Inserts a new actuator command into the actuator_commands table.
    """
    try:
        if timestamp is None:
            timestamp = datetime.utcnow().isoformat() + "Z"

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO actuator_commands (node_id, actuator_type, action, source, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, (node_id, actuator_type, action, source, timestamp))
        conn.commit()
        conn.close()
        logger.info(f"Logged actuator command: {node_id} {actuator_type} {action} from {source} at {timestamp}")
    except Exception as e:
        logger.error(f"Error logging actuator command: {e}")