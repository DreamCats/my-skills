from __future__ import annotations

import argparse

from config import (
    DEFAULT_BROWSER_URL,
    DEFAULT_PROTOCOL_VERSION,
    DEFAULT_TIMEOUT_MS,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Chrome DevTools MCP Python client")
    parser.add_argument(
        "--browser-url",
        default=DEFAULT_BROWSER_URL,
        help="Remote debugging URL to connect to (default: %(default)s).",
    )
    parser.add_argument(
        "--no-prefer-running",
        action="store_true",
        help="Always start a new Chrome instead of checking for an existing one.",
    )
    parser.add_argument(
        "--require-browser",
        action="store_true",
        help="Fail if no debuggable Chrome is detected at --browser-url.",
    )
    parser.add_argument("--headless", action="store_true", help="Start Chrome headless.")
    parser.add_argument("--quiet", action="store_true", help="Suppress informational warnings.")
    parser.add_argument(
        "--channel",
        choices=["stable", "beta", "dev", "canary"],
        help="Chrome channel to launch.",
    )
    parser.add_argument("--user-data-dir", help="Chrome user data directory.")
    parser.add_argument("--isolated", action="store_true", help="Use an isolated profile.")
    parser.add_argument("--viewport", help="Viewport size, e.g. 1280x720.")
    parser.add_argument("--server-log", help="Write MCP server logs to file.")
    parser.add_argument(
        "--chrome-arg",
        action="append",
        help="Extra Chrome argument (repeatable).",
    )
    parser.add_argument(
        "--protocol-version",
        default=DEFAULT_PROTOCOL_VERSION,
        help="MCP protocol version to use.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("status", help="Show connection and reuse status")

    subparsers.add_parser("list-tools", help="List available MCP tools")

    call_parser = subparsers.add_parser("call", help="Call any tool by name")
    call_parser.add_argument("--name", required=True, help="Tool name")
    call_parser.add_argument("--json", help="Tool arguments in JSON")

    new_page = subparsers.add_parser("new-page", help="Open a new page")
    new_page.add_argument("--url", required=True, help="Target URL")
    new_page.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT_MS, help="Timeout in ms"
    )

    navigate = subparsers.add_parser("navigate", help="Navigate current page")
    navigate.add_argument("--url", required=True, help="Target URL")
    navigate.add_argument(
        "--timeout", type=int, default=DEFAULT_TIMEOUT_MS, help="Timeout in ms"
    )
    navigate.add_argument("--ignore-cache", action="store_true", help="Ignore cache")

    snapshot = subparsers.add_parser("snapshot", help="Take a snapshot")
    snapshot.add_argument("--out", help="Output file path")
    snapshot.add_argument("--verbose", action="store_true", help="Include full a11y tree")

    screenshot = subparsers.add_parser("screenshot", help="Take a screenshot")
    screenshot.add_argument("--out", help="Output file path")
    screenshot.add_argument(
        "--format",
        choices=["png", "jpeg", "webp"],
        default="png",
        help="Screenshot format",
    )
    screenshot.add_argument("--full-page", action="store_true", help="Full page screenshot")
    screenshot.add_argument("--quality", type=int, help="JPEG/WebP quality (0-100)")
    screenshot.add_argument("--uid", help="Element uid to capture")

    click = subparsers.add_parser("click", help="Click an element")
    click.add_argument("--uid", required=True, help="Element uid")
    click.add_argument("--double", action="store_true", help="Double click")

    fill = subparsers.add_parser("fill", help="Fill an input")
    fill.add_argument("--uid", required=True, help="Element uid")
    fill.add_argument("--value", required=True, help="Value to fill")

    press = subparsers.add_parser("press", help="Press a key")
    press.add_argument("--key", required=True, help="Key or key combo")

    wait = subparsers.add_parser("wait", help="Wait for text to appear")
    wait.add_argument("--text", help="Text to wait for")
    wait.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_MS, help="Timeout in ms")

    subparsers.add_parser("list-pages", help="List pages")

    select_page = subparsers.add_parser("select-page", help="Select page by index")
    select_page.add_argument("--index", type=int, required=True, help="Page index")
    select_page.add_argument("--bring-to-front", action="store_true", help="Focus page")

    close_page = subparsers.add_parser("close-page", help="Close page by index")
    close_page.add_argument("--index", type=int, required=True, help="Page index")

    list_console = subparsers.add_parser("list-console", help="List console messages")
    list_console.add_argument("--page-idx", type=int, help="Page index")
    list_console.add_argument("--page-size", type=int, help="Page size")
    list_console.add_argument("--include-preserved", action="store_true")
    list_console.add_argument("--types", nargs="*", help="Filter by message types")

    list_network = subparsers.add_parser("list-network", help="List network requests")
    list_network.add_argument("--page-idx", type=int, help="Page index")
    list_network.add_argument("--page-size", type=int, help="Page size")
    list_network.add_argument("--include-preserved", action="store_true")
    list_network.add_argument("--resource-types", nargs="*", help="Filter resource types")

    trace_start = subparsers.add_parser("trace-start", help="Start performance trace")
    trace_start.add_argument("--auto-stop", action="store_true", help="Auto stop trace")
    trace_start.add_argument("--reload", action="store_true", help="Reload on start")

    trace_stop = subparsers.add_parser("trace-stop", help="Stop performance trace")
    trace_stop.add_argument("--out", help="Output file path")

    trace_insight = subparsers.add_parser("trace-insight", help="Analyze a trace insight")
    trace_insight.add_argument("--name", required=True, help="Insight name")
    trace_insight.add_argument("--set-id", required=True, help="Insight set id")

    return parser
