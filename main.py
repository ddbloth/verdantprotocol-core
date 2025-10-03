# main.py

import logging
from mqtt.client import create_mqtt_client

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)

def main():
    logging.info("Starting VerdantProtocol Master Controller...")

    # Create and start MQTT client
    mqtt_client = create_mqtt_client()

    # Blocking loop to keep the client running
    mqtt_client.loop_forever()

if __name__ == "__main__":
    main()