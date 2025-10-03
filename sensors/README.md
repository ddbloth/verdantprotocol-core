# Sensors

This directory contains code for parsing and validating sensor telemetry that arrives over MQTT. The main module is `parser.py` which turns raw MQTT payloads into structured readings the rest of the system understands.

This README explains the parser "contract", expected payload shapes, testing tips, and how to add support for new sensor types.

## Purpose

- Normalize incoming sensor messages into a consistent Reading object/dict.
- Validate required fields and basic sanity checks (types, ranges).
- Provide helpful errors for malformed payloads so calling code can choose to log, ignore, or retry.

## Key file

- `parser.py` — contains the parser functions used by the MQTT client. Look for functions named like `parse_*` and a top-level `parse_message` or `parse_payload` entry point.

If you change how parsing works, update `tests/test_parser.py` accordingly.

## Parser contract (tiny)

Inputs
- raw payload: bytes or string (the raw payload delivered by the MQTT client)
- topic: the MQTT topic string (optional, used to infer node id or sensor channel)

Outputs
- On success: a dict-like Reading with these keys (example):
  - `node_id` (str) — unique id for the sensor node
  - `ts` (int | float) — unix timestamp in seconds (float allowed)
  - `sensor` (str) — sensor type or channel (e.g. `temp`, `soil_moisture`)
  - `value` (number|string|bool) — the measured value
  - `meta` (dict, optional) — extra metadata (battery, rssi, raw)

- On failure: raise a `ValueError` (or return `None` depending on current project convention). See the tests to confirm which approach the codebase expects.

Error modes
- Malformed JSON
- Missing required fields (node id, value)
- Wrong type (e.g., string where number expected)

Design notes
- Keep parsing logic deterministic and fast.
- Prefer explicit validation and clear exceptions so the MQTT client or caller can decide what to do with bad messages.

## Example payloads

- JSON sensor payload (temperature sensor):

```json
{
  "node_id": "node-abc123",
  "ts": 1690000000,
  "sensor": "temp",
  "value": 23.7,
  "meta": { "battery": 3.7, "rssi": -60 }
}
```

- Compact payload (string) used by some Pico W devices:

```
node-abc123|temp|1690000000|23.7
```

The parser should support the formats your fleet publishes. If you add another format, add a test case.

## Data shape and validation checklist

- `node_id`: non-empty string
- `ts`: present and a positive integer/float; if missing, parser may insert current time
- `sensor`: string; must be one of the recognized sensor channels (extendable)
- `value`: numeric for analog sensors; boolean for switches; string for state labels

Edge cases to test
- Empty payload
- Non-JSON payload when JSON expected
- JSON missing `node_id` or `value`
- Value out of expected range (e.g. negative humidity)
- Duplicate messages (idempotency is handled elsewhere)

## Running parser tests

From the repository root, run the focused parser tests:

```bash
pytest -q tests/test_parser.py
```

Add new tests that assert on the exact Reading structure to avoid regressions.

## How to add support for a new sensor type

1. Add parsing logic in `parser.py` (prefer small helper function `parse_<format_or_sensor>`).
2. Update any canonical list of allowed `sensor` names (if present).
3. Add unit tests in `tests/test_parser.py` covering:
   - successful parse
   - missing/invalid fields
   - boundary values
4. Run the test suite and make sure lints/types (if any) pass.

## Integration with MQTT and rules

- The MQTT client (`mqtt/client.py`) should call into this parser to transform payloads before passing them down the pipeline.
- The output Reading should be compatible with `automation/rules.py` expectations (check the rules code to confirm exact keys and types).

## Debugging tips

- Log raw payloads when new node types are added so you can capture sample data.
- Add a small script or REPL snippet to call the parser with saved payloads while iterating on parsing logic. Example (from project root):

```python
from sensors import parser

raw = open('tests/fixtures/sample_payload.json').read()
print(parser.parse_payload(raw, topic='sensors/node-abc123'))
```

## Where to look next

- `tests/test_parser.py` — example inputs and expected outputs.
- `mqtt/topics.py` — topic naming conventions that may encode node id or sensor channel.

If you want, I can:

- Add a `fixtures/` directory under `tests/` with sample payloads and a small helper that loads them for tests.
- Add a `parser.md` with more detailed examples per sensor type.

Tell me which you'd prefer and I will implement it.
