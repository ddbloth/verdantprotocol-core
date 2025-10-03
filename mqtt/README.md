# MQTT

This directory contains MQTT-related code for VerdantProtocol's core controller. It centralizes topic definitions and the client glue that subscribes to sensor topics, publishes actuator commands, and dispatches messages into the rest of the system.

Files

- `client.py` — MQTT client wrapper used by `main.py` to connect to a broker, subscribe to topics, and call parsing/handler functions.
- `topics.py` — canonical topic names, topic patterns, and helpers for building topic strings used across the repo.

Goals for this module

- Provide a small, testable wrapper over whatever MQTT library is chosen (paho-mqtt is common for Python).
- Keep topic names centralized so tests, automation rules, and actuators use the same strings.
- Provide clear boundaries so tests can replace the client with a stub or an in-process test double.

Configuration

The controller reads MQTT connection information from the environment or a configuration layer. Typical environment variables you may see or want to support:

- `MQTT_BROKER` — broker hostname or IP (e.g. `localhost` or `10.0.0.5`)
- `MQTT_PORT` — broker TCP port (usually `1883` for unencrypted or `8883` for TLS)
- `MQTT_USER` / `MQTT_PASS` — optional credentials
- `MQTT_KEEPALIVE` — keepalive seconds
- `MQTT_CLIENT_ID` — client id used to connect

Check `mqtt/client.py` to confirm the exact variable names and any defaults. If you prefer, you can add a `config.example.env` at repo root and load it at runtime.

Run a local broker for development

You can use Mosquitto (locally installed) or run one in Docker for quick testing.

Docker example (runs mosquitto on host port 1883):

```bash
docker run -d --name mosquitto -p 1883:1883 eclipse-mosquitto:2
```

Then run the core controller with environment variables pointing at `localhost`.

Common patterns and MQTT concepts used by the project

- Topics and topic filters — use `+` and `#` where appropriate; `topics.py` centralizes these strings.
- QoS — choose the quality of service depending on sensor reliability and network constraints.
- Retained messages — avoid relying on retained messages for transient telemetry; prefer state topics for configuration or presence.
- Last Will and Testament — useful for signaling node disconnects.

Publishing and subscribing

The client wrapper provides higher-level functions for:

- subscribe(topic, callback)
- publish(topic, payload, qos=0, retain=False)
- start() / stop() life-cycle helpers

Design notes for contributions

- Keep the client thin: individual business logic (parsing, rule evaluation) should live outside the MQTT client.
- Accept an injectable client object for testing. Tests should be able to create a fake client that records publishes and triggers callbacks.

Testing advice

- Unit tests: monkeypatch or stub the underlying paho/mqtt client used in `mqtt/client.py`. Replace network calls with in-memory handlers.
- Integration tests: run a disposable broker (see Docker example) and use a real client to verify end-to-end flows.
- Use pytest fixtures to provide a temporary broker host/port or a fake client implementation.

Example MQTT testing fixture (concept sketch for `tests/conftest.py`):

```python
class DummyClient:
    def __init__(self):
        self.subscriptions = {}
        self.published = []

    def publish(self, topic, payload, qos=0, retain=False):
        self.published.append((topic, payload, qos, retain))

    def simulate_message(self, topic, payload):
        # call subscribed callbacks
        if topic in self.subscriptions:
            for cb in self.subscriptions[topic]:
                cb(topic, payload)

    def subscribe(self, topic, callback):
        self.subscriptions.setdefault(topic, []).append(callback)

# In tests, inject DummyClient into mqtt.client module or use monkeypatch
```

Where to learn about MQTT

If you or contributors are new to MQTT, here are concise, high-quality resources to learn the protocol and best practices:

- MQTT.org — official site: https://mqtt.org/ (specs, introductions)
- Eclipse Mosquitto — broker documentation and examples: https://mosquitto.org/
- Eclipse Paho (client libraries) — Python client docs: https://www.eclipse.org/paho/
- A friendly tutorial: HiveMQ MQTT Essentials: https://www.hivemq.com/mqtt-essentials/
- MQTT 5.0 features (if you plan to use MQTT 5): https://mqtt.org/new-classification/ (or the MQTT 5 specification linked from mqtt.org)

These resources explain topics, QoS, retained messages, session state, and how to use client libraries in practice.

Examples and debugging

- Use `mosquitto_sub` and `mosquitto_pub` to inspect and publish messages while developing.

```bash
mosquitto_sub -h localhost -t "#" -v
mosquitto_pub -h localhost -t "sensors/node-1/temp" -m '{"node_id":"node-1","sensor":"temp","ts":1690000000,"value":22.1}'
```

- Add verbose logging in `mqtt/client.py` to record subscriptions, incoming payloads, and published messages while debugging.

Security and production notes

- For production, prefer TLS connections (port 8883) and certificate verification.
- Use authenticated brokers with appropriate access control lists (ACLs) to restrict who can publish/subscribe to critical topics.
- Consider using last-will messages to detect node failures and implement reconnection/backoff strategies for flaky networks.

Next steps I can help with

- Add a `config.example.env` in the repo that lists the MQTT environment variables used by `mqtt/client.py`.
- Create a `tests/conftest.py` fixture that provides a `DummyClient` and wiring for the existing tests.
- Add a small `examples/` script that publishes example sensor messages for manual testing.

Tell me which you'd like and I'll implement it next.
