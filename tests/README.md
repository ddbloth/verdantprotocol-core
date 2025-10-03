# Tests — verdantprotocol-core

This directory contains unit and integration tests for the `verdantprotocol-core` project. The suite is written for pytest and covers the parser, MQTT-related helpers, automation rules, logging utilities, and an end-to-end sensor->actuator flow.

## What is here

- `test_parser.py` — tests for `sensors/parser.py` (payload parsing, validation).
- `test_mqtt_flow.py` — tests for MQTT client helpers and topic handling.
- `test_rules.py` — rule evaluation and edge cases for `automation/rules.py`.
- `test_logger.py` — tests for `utils/logger.py` and persistence behavior.
- `test_sensor_actuator_flow.py` — higher-level flow tests that simulate sensor input and expect actuator commands.

If you add tests, keep filenames prefixed with `test_` and put helper fixtures or test utilities in `conftest.py` (create one if needed).

## Running tests locally

Activate your virtual environment (see repo top-level README for recommended venv):

```bash
# from the repository root, if using the top-level venv
source ../.vp-venv/bin/activate

# or a repo-local venv
source .venv/bin/activate
```

Install dependencies (if you haven't already):

```bash
pip install -r requirements.txt
pip install pytest
```

Run the whole suite:

```bash
pytest -q
```

Run a single test file or module:

```bash
pytest tests/test_parser.py -q
```

Run a single test function:

```bash
pytest tests/test_parser.py::test_parse_valid_payload -q
```

Run tests with increased verbosity or show print output:

```bash
pytest -q -r a -s
```

Run a subset by keyword:

```bash
pytest -k mqtt -q
```

## Database and state isolation

Tests in this repo may touch `data/logs.db`. To avoid test interference:

- Use fixtures to create a temporary copy of the DB or to point the application at a temporary SQLite file (e.g. `tmp_path / "test_logs.db"`).
- If tests directly modify `data/logs.db`, ensure each test cleans up after itself or reset the DB in a `setup`/`teardown` fixture.

Example fixture sketch (in `conftest.py`):

```python
import shutil
from pathlib import Path

import pytest

@pytest.fixture(autouse=True)
def tmp_db(tmp_path, monkeypatch):
    src = Path(__file__).parent.parent / "data" / "logs.db"
    dst = tmp_path / "logs.db"
    shutil.copy(src, dst)
    # monkeypatch or set config so the code uses dst path for DB
    monkeypatch.setenv("VERDANT_DB_PATH", str(dst))
    return dst
```

## MQTT and external services

The tests avoid contacting a real MQTT broker. Use one of these approaches:

- Monkeypatch or inject a fake MQTT client in tests (replace `mqtt.client`'s client instance with a stub that records published messages).
- Use a lightweight in-process broker or test double library if you need protocol-level testing.

Example: use `monkeypatch` to replace the publish method with a recorder object.

## Coverage and CI

To collect coverage locally:

```bash
pip install pytest-cov
pytest --cov=verdantprotocol_core --cov-report=term-missing
```

For CI (GitHub Actions) you can run the above and publish coverage. A minimal job would:

- Set up Python
- Install dependencies
- Run `pytest --cov ...`

## Writing good tests

- Prefer small, focused unit tests for parsing, rule math, and single-function behavior.
- Use higher-level integration tests sparingly; make them deterministic by mocking external endpoints.
- Add tests for edge cases (empty payloads, malformed JSON, missing fields, boundary threshold values for rules).
- Keep tests fast; aim for sub-second unit tests when possible.

## When tests fail

- Run the failing tests directly to get clearer tracebacks.
- Use `-k` to run related tests when diagnosing a failing area.
- If failures are due to environment (missing env vars, no venv), confirm the virtualenv and installed deps.

## Contributing tests

1. Add the test file under `tests/` following the naming convention.
2. Add or update fixtures in `conftest.py` to share common setup/teardown.
3. Run `pytest` locally and iterate until green.
4. Open a PR and include any rationale for added tests.

---

If you want, I can also:

- Add a `conftest.py` with helpful fixtures for DB and MQTT stubs.
- Add a GitHub Actions workflow that runs pytest and publishes coverage.

Feel free to tell me which you'd like me to add next.
