from __future__ import annotations

import os
import sys
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional

from config import DEFAULT_USER_DATA_DIR, ServerConfig


def probe_browser_url(browser_url: str, timeout: float = 0.8) -> bool:
    check_url = browser_url.rstrip("/")
    if not check_url.endswith("/json/version"):
        check_url = check_url + "/json/version"
    try:
        with urllib.request.urlopen(check_url, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            return True
    except (urllib.error.URLError, ValueError):
        return False


def resolve_user_data_dir(config: ServerConfig) -> Optional[str]:
    if config.user_data_dir:
        return config.user_data_dir
    if config.isolated:
        return None
    return DEFAULT_USER_DATA_DIR


def read_devtools_port(user_data_dir: str) -> Optional[int]:
    if not user_data_dir:
        return None
    path = os.path.join(user_data_dir, "DevToolsActivePort")
    try:
        with open(path, "r", encoding="utf-8") as handle:
            line = handle.readline().strip()
            return int(line)
    except (OSError, ValueError):
        return None


def build_status(config: ServerConfig) -> Dict[str, Any]:
    effective_user_data_dir = resolve_user_data_dir(config)
    browser_url_ok = False
    if config.browser_url:
        browser_url_ok = probe_browser_url(config.browser_url)
    devtools_port = read_devtools_port(effective_user_data_dir or "")
    devtools_url = f"http://127.0.0.1:{devtools_port}" if devtools_port else None
    devtools_url_ok = False
    if devtools_url:
        devtools_url_ok = probe_browser_url(devtools_url)

    if config.prefer_running:
        if browser_url_ok:
            strategy = "reuse-browser-url"
        elif devtools_url_ok:
            strategy = "reuse-devtools-port"
        else:
            strategy = "launch-new"
    else:
        strategy = "launch-new"

    return {
        "browser_url": config.browser_url,
        "browser_url_reachable": browser_url_ok,
        "devtools_port": devtools_port,
        "devtools_url": devtools_url,
        "devtools_url_reachable": devtools_url_ok,
        "user_data_dir": effective_user_data_dir,
        "prefer_running": config.prefer_running,
        "require_browser": config.require_browser,
        "strategy": strategy,
        "require_browser_would_fail": config.require_browser and strategy == "launch-new",
    }


def build_server_args(config: ServerConfig) -> List[str]:
    args = ["-y", "chrome-devtools-mcp@latest"]

    browser_url = config.browser_url
    use_browser_url = False
    effective_user_data_dir = resolve_user_data_dir(config)

    if config.prefer_running and browser_url:
        if probe_browser_url(browser_url):
            use_browser_url = True
        else:
            browser_url = None

    if config.prefer_running and not use_browser_url:
        devtools_port = read_devtools_port(effective_user_data_dir or "")
        if devtools_port:
            candidate_url = f"http://127.0.0.1:{devtools_port}"
            if probe_browser_url(candidate_url):
                browser_url = candidate_url
                use_browser_url = True

    if config.require_browser and not use_browser_url:
        target = config.browser_url or "existing Chrome (DevToolsActivePort)"
        raise RuntimeError(
            "No debuggable Chrome detected at "
            f"{target}. Start Chrome with --remote-debugging-port=9222 "
            "or pass --browser-url, or omit --require-browser to auto-launch."
        )
    if config.prefer_running and not use_browser_url and not config.quiet:
        print(
            "No debuggable Chrome detected; starting a new Chrome instance. "
            "Tip: launch Chrome with --remote-debugging-port=9222 or pass "
            "--browser-url to reuse an existing session.",
            file=sys.stderr,
        )

    if use_browser_url:
        args.append(f"--browser-url={browser_url}")

    if config.headless:
        args.append("--headless")
    if config.channel:
        args.append(f"--channel={config.channel}")
    if not use_browser_url:
        if effective_user_data_dir:
            args.append(f"--user-data-dir={effective_user_data_dir}")
        if config.isolated:
            args.append("--isolated")
    if config.viewport:
        args.append(f"--viewport={config.viewport}")
    if config.log_file:
        args.append(f"--log-file={config.log_file}")
    for extra in config.chrome_args:
        args.append(f"--chrome-arg={extra}")
    return args
