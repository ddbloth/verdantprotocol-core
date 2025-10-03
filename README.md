# 🌿 verdantprotocol-core

Core master-controller code for VerdantProtocol: MQTT glue, parsing, logging, automation rules, actuators, and an optional dashboard. This repo is intended to run on a Pi-class device (development notes use Raspberry Pi 5) and coordinate sensor nodes and actuators over MQTT.

This README is a concise entrypoint — detailed, implementation-level documentation now lives in each package's README. See the "Module docs" section below.

## Quick links

- Automation rules and actuators: `automation/README.md`
- MQTT client and topics: `mqtt/README.md`
- Sensor parsing: `sensors/README.md`
- Tests and testing guidance: `tests/README.md`

## Repo layout (high level)

- `main.py` — run the controller (subscribe to MQTT, run automation loop)
- `requirements.txt` — Python dependencies
- `automation/`, `mqtt/`, `sensors/`, `utils/`, `dashboard/` — functional modules (see module READMEs)
- `data/logs.db` — local SQLite file used for development history
- `tests/` — pytest suite

## Quick start

Activate the shared top-level virtualenv (convention used in this workspace):

```bash
# from repository root (if .vp-venv exists in the parent folder)
source ../.vp-venv/bin/activate
```

Or create and use a repo-local venv:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the controller:

```bash
python main.py
```

Run tests:

```bash
pytest -q
```

## Configuration & environment

The project prefers minimal code-driven configuration. Common environment variables you may encounter:

- `MQTT_BROKER`, `MQTT_PORT`, `MQTT_USER`, `MQTT_PASS` — MQTT connection settings (see `mqtt/client.py`)
- `VERDANT_DB_PATH` — path to the SQLite DB (if you want to use a different file)

Consider creating a `config.example.env` or a small `config.yaml` if you want to centralize runtime options — I can add one if you'd like.

## How the pieces fit together (short)

- Sensor nodes publish telemetry to MQTT topics.
- The MQTT client (`mqtt/client.py`) receives messages and calls the parser in `sensors/parser.py`.
- Parsed readings are persisted and evaluated by rules in `automation/rules.py`.
- When a rule triggers, commands are sent to actuators (via `automation/actuators.py` and MQTT topics).

## Contributing

Open PRs with small, focused changes and tests. Add or update module-level documentation when you change behavior. See the module READMEs for testing and development tips.

## Notes / TODOs

- Add a runtime config example (`config.example.env` or `config.example.yaml`).
- Add a systemd service example for running on Raspberry Pi.
- Consider expanding the dashboard and adding authentication for remote access.

## License

MIT

## Contact / Author

Maintained by the VerdantProtocol project. See the parent workspace for other repos (nodes, actuators) and developer notes.
