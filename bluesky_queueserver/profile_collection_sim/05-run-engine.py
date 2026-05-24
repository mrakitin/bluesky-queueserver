# flake8: noqa
print(f"Loading file {__file__!r}")

import os

from bluesky import RunEngine
from bluesky.callbacks.best_effort import BestEffortCallback

from bluesky_queueserver import is_ipython_mode

# Detect if the code is executed in IPython environment and backend uses Qt
ipython_matplotlib = False
try:
    import matplotlib

    if matplotlib.get_backend().startswith("qt"):
        ipython_matplotlib = True
except Exception:
    pass

RE = RunEngine({"metadata_key": "metadata_value"})

bec = BestEffortCallback()
if not is_ipython_mode() or not ipython_matplotlib:
    bec.disable_plots()

RE.subscribe(bec)

# Subscribe the RunEngine to a local Tiled server (if running).
# Start the server with: pixi run start-tiled-server
# Independent clients can read without auth: from tiled.client import from_uri; c = from_uri("http://localhost:8000")
_TILED_URI = os.environ.get("TILED_URI", "http://localhost:8000")
_TILED_API_KEY = os.environ.get("TILED_API_KEY", "bluesky")

try:
    import httpx as _httpx

    _httpx.get(_TILED_URI, timeout=2.0)  # fast reachability check before the retrying client
    from bluesky_tiled_plugins import TiledWriter

    _tiled_writer = TiledWriter.from_uri(_TILED_URI, api_key=_TILED_API_KEY)
    RE.subscribe(_tiled_writer)
    print(f"RunEngine subscribed to Tiled server at {_TILED_URI}")
except Exception as _tiled_exc:
    print(f"WARNING: Could not subscribe RunEngine to Tiled server at {_TILED_URI}: {_tiled_exc}")
