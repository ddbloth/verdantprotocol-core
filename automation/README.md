# Automation

This directory contains automation logic: the rules that decide when to take action and the actuator wrappers that send commands to devices. Keep rules declarative where possible and small helper code in `actuators.py`.

Files

- `rules.py` — automation rules and evaluation engine. This file contains the logic that inspects sensor readings and decides whether to trigger actuators.
- `actuators.py` — thin wrappers that translate intent (e.g. "turn pump on") into MQTT or hardware commands.

Why this directory exists

- Provide a single place to define, test, and reason about automation behavior.
- Keep side-effects (publishing MQTT, toggling GPIOs) inside `actuators.py` so `rules.py` can be unit tested without networking or hardware.

Tiny contract (inputs / outputs / errors)

- Inputs: one or more structured Reading objects produced by the parser (see `sensors/parser.py`). Typical shape:
  - `node_id` (str), `ts` (int/float), `sensor` (str), `value` (number|string|bool), `meta` (dict)
- Outputs: a list of zero-or-more Actuation commands. An Actuation command is a dict (or simple object) with keys like:
  - `target` (str) — actuator id or topic
  - `command` (str) — action name (e.g. `on`, `off`, `set`) 
  - `args` (dict, optional) — extra params (duration, value)
- Error modes: invalid/malformed readings, missing device mappings, failed actuator publish. Rules should raise well-defined exceptions or return an empty action list when they cannot decide.

Success criteria

- Rules are deterministic and stateless (rules evaluate request -> response without hidden side-effects).
- Actuators perform side-effects; their operations should be idempotent where possible.

Rule design patterns

- Threshold rule: trigger when a sensor value crosses a threshold and optionally apply hysteresis to avoid chattering.
- Time-window rule: consider averages or counts over a time window before acting (helpful to avoid reacting to single noisy samples).
- Composite rule: combine multiple sensor inputs (e.g. temperature AND humidity) before acting.

Example rule (conceptual)

```python
def check_soil_moisture(reading):
    # reading: { node_id, sensor, value, ts }
    if reading['sensor'] != 'soil_moisture':
        return []
    if reading['value'] < 0.30:  # 30% threshold
        return [
            { 'target': 'pump-zone-1', 'command': 'on', 'args': { 'duration_s': 10 } }
        ]
    return []
```

Hysteresis example

Only turn the pump back on when moisture falls below 30%, but don't turn it off until moisture rises above 36%.

Actuator interface notes

- Keep `actuators.py` as the single place that knows how to: map `target` -> MQTT topic or GPIO, serialize commands, and handle retries/confirmation.
- Actuator functions should accept simple command dicts and return a result object: `{ 'ok': True, 'info': ... }` or `{ 'ok': False, 'error': '...' }`.

Testing automation

- Unit tests for `rules.py`: provide synthetic readings and assert the returned command list matches expectations. These tests should not require MQTT or the database.
- Unit tests for `actuators.py`: inject a fake MQTT client (or monkeypatch the publish function) and assert publishes are correct.
- Integration tests: use a temporary broker (or an in-process stub) and verify end-to-end behavior (sensor -> rule -> publish).

Example test snippet for rules (pytest)

```python
from automation.rules import check_soil_moisture

def test_soil_trigger():
    reading = { 'node_id': 'node-1', 'sensor': 'soil_moisture', 'value': 0.2, 'ts': 0 }
    actions = check_soil_moisture(reading)
    assert actions and actions[0]['target'] == 'pump-zone-1'
```

Debouncing and scheduling

- Avoid immediate, repeated actuation: schedule repeating checks or record the last actuation timestamp and refuse to re-fire within a cooldown window.
- For longer operations (e.g., run pump for N seconds), have actuators accept duration and the actuator layer implement timers.

Operational considerations

- Logging: record rule evaluations and actuator commands (with timestamps) so operator can audit decisions.
- Safety: include safe-fail behaviors (e.g., if an actuator command fails, log and optionally escalate via alert topic).

Extending with new rules or actuators

1. Add small, focused functions in `rules.py` or add a new module under `automation/`.
2. Add unit tests in `tests/` covering happy path and edge cases.
3. If adding an actuator type (new hardware), implement mapping and serialization in `actuators.py` and add tests that assert published messages.

Contributing tips

- Keep functions pure where possible.
- Add docstrings that explain the intent of each rule.
- Keep side-effects in `actuators.py` and out of rules to make rules easy to test.

Next steps I can help with

- Create a small `automation/config.example.yaml` that lists rule parameters (thresholds, hysteresis, cooldowns) and show how to load it.
- Add a basic scheduling/cooldown helper and tests to prevent chattering.
- Add an example rule set file and a test harness that simulates a stream of readings.

Tell me which you'd like and I'll implement it.
