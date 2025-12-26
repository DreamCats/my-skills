from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional

DEFAULT_BROWSER_URL = "http://127.0.0.1:9222"
DEFAULT_PROTOCOL_VERSION = "2024-11-05"
DEFAULT_LOG_DIR = os.path.expanduser("~/.chrome_mcp/logs")
DEFAULT_USER_DATA_DIR = os.path.expanduser("~/.chrome_mcp/chrome-profile")
DEFAULT_TIMEOUT_MS = 120000


@dataclass
class ServerConfig:
    browser_url: Optional[str]
    prefer_running: bool
    require_browser: bool
    headless: bool
    channel: Optional[str]
    user_data_dir: Optional[str]
    isolated: bool
    viewport: Optional[str]
    log_file: Optional[str]
    chrome_args: List[str]
    protocol_version: Optional[str]
    quiet: bool


def ensure_log_dir() -> str:
    os.makedirs(DEFAULT_LOG_DIR, exist_ok=True)
    return DEFAULT_LOG_DIR


def default_output_path(prefix: str, suffix: str) -> str:
    ensure_log_dir()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    return os.path.join(DEFAULT_LOG_DIR, f"{prefix}_{ts}{suffix}")


def print_json(data: Dict[str, Any]) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def has_tool_error(result: Dict[str, Any]) -> bool:
    return bool(result.get("isError"))


def normalize_timeout_ms(timeout_ms: Optional[int], quiet: bool, label: str) -> Optional[int]:
    if timeout_ms is None:
        return None
    if timeout_ms == 0:
        return 0
    if timeout_ms < 1000:
        adjusted = timeout_ms * 1000
        if not quiet:
            print(
                f"Timeout value {timeout_ms} for {label} looks like seconds; "
                f"interpreting as {adjusted} ms.",
                file=sys.stderr,
            )
        return adjusted
    return timeout_ms
