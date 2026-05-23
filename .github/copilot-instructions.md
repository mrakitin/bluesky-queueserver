# bluesky-queueserver — Copilot Instructions

## Environment setup

This repository uses [pixi](https://pixi.sh) to manage the Python environment (Python 3.12, conda-forge).

### First-time setup

```bash
pixi install          # resolve and install all dependencies
pixi run install      # install the package itself in editable mode (pip install -e .)
```

### Running commands

Always use `pixi run` to invoke tools inside the managed environment:

```bash
pixi run python       # Python interpreter
pixi run pytest       # run tests
pixi run qserver      # qserver CLI
pixi run start-re-manager  # start the RE manager
```

Or open an interactive shell with the environment activated:

```bash
pixi shell
```

### Running tests

Most unit tests need no external services:

```bash
pixi run python -m pytest bluesky_queueserver/manager/tests/test_annotation_decorator.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_json_rpc.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_utils.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_config.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_comms.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_conversions.py
pixi run python -m pytest bluesky_queueserver/manager/tests/test_logging.py
```

Tests that exercise the plan queue (`test_plan_queue_ops.py`) require a running **Redis** server on `localhost:6379`.

#### Start Redis (macOS with Homebrew)

```bash
brew services start redis
```

#### Start Redis (Linux / CI)

Use the Docker service in the GitHub Actions workflow (already configured in `copilot-setup-steps.yml`), or:

```bash
docker run -d -p 6379:6379 redis:latest
```

### Known flaky tests (pre-existing timing issues on macOS ARM)

These tests are sensitive to CPU/IO timing and may fail on Apple Silicon:

- `test_comms.py::test_PipeJsonRpcReceive_5[False-*]`
- `test_comms.py::test_ZMQCommSendAsync_4[0.1-*]`

Deselect them when running the full suite locally:

```bash
pixi run python -m pytest bluesky_queueserver/manager/tests/ \
  --deselect bluesky_queueserver/manager/tests/test_comms.py::test_PipeJsonRpcReceive_5 \
  --deselect "bluesky_queueserver/manager/tests/test_comms.py::test_ZMQCommSendAsync_4[0.1-True-False-msgpack]" \
  --deselect "bluesky_queueserver/manager/tests/test_comms.py::test_ZMQCommSendAsync_4[0.1-True-True-json]" \
  --deselect "bluesky_queueserver/manager/tests/test_comms.py::test_ZMQCommSendAsync_4[0.1-True-True-msgpack]" \
  --deselect "bluesky_queueserver/manager/tests/test_comms.py::test_ZMQCommSendAsync_4[0.1-False2-False-json]"
```
