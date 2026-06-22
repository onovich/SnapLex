"""Local application data path helpers."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path


APP_DATA_DIR_ENV_VAR = "SNAPLEX_APP_DATA_DIR"


def default_app_data_dir(environ: Mapping[str, str] | None = None) -> Path:
    """Return the local app data directory without creating it."""

    env = os.environ if environ is None else environ
    override = env.get(APP_DATA_DIR_ENV_VAR, "").strip()
    if override:
        return Path(override).expanduser()

    appdata = env.get("APPDATA", "").strip()
    if appdata:
        return Path(appdata).expanduser() / "SnapLex"

    return Path.home() / ".snaplex"
