from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict

from browser_session import build_server_args, build_status
from cli import build_parser
from config import (
    DEFAULT_TIMEOUT_MS,
    ServerConfig,
    default_output_path,
    has_tool_error,
    normalize_timeout_ms,
    print_json,
)
from mcp_client import MCPClient
from wait_utils import wait_for_ready_state


def run_command(args: argparse.Namespace) -> int:
    server_config = ServerConfig(
        browser_url=args.browser_url,
        prefer_running=not args.no_prefer_running,
        require_browser=args.require_browser,
        headless=args.headless,
        channel=args.channel,
        user_data_dir=args.user_data_dir,
        isolated=args.isolated,
        viewport=args.viewport,
        log_file=args.server_log,
        chrome_args=args.chrome_arg or [],
        protocol_version=args.protocol_version,
        quiet=args.quiet,
    )

    if args.command == "status":
        print_json(build_status(server_config))
        return 0

    server_args = build_server_args(server_config)
    client = MCPClient("npx", server_args, server_config.protocol_version)
    try:
        client.start()
        client.initialize()

        if args.command == "list-tools":
            result = client.list_tools()
            print_json(result)
            return 0

        if args.command == "call":
            payload = json.loads(args.json) if args.json else {}
            result = client.call_tool(args.name, payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "new-page":
            payload = {"url": args.url}
            timeout_ms = normalize_timeout_ms(args.timeout, args.quiet, "new-page")
            if timeout_ms is not None:
                payload["timeout"] = timeout_ms
            result = client.call_tool("new_page", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "navigate":
            payload: Dict[str, Any] = {"type": "url", "url": args.url}
            timeout_ms = normalize_timeout_ms(args.timeout, args.quiet, "navigate")
            if timeout_ms is not None:
                payload["timeout"] = timeout_ms
            if args.ignore_cache:
                payload["ignoreCache"] = True
            result = client.call_tool("navigate_page", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "snapshot":
            out_path = args.out or default_output_path("snapshot", ".txt")
            payload = {"filePath": out_path}
            if args.verbose:
                payload["verbose"] = True
            result = client.call_tool("take_snapshot", payload)
            print_json(result)
            if not has_tool_error(result):
                print(out_path)
                return 0
            return 1

        if args.command == "screenshot":
            suffix = ".png" if args.format == "png" else f".{args.format}"
            out_path = args.out or default_output_path("screenshot", suffix)
            payload: Dict[str, Any] = {"filePath": out_path, "format": args.format}
            if args.full_page:
                payload["fullPage"] = True
            if args.quality is not None:
                payload["quality"] = args.quality
            if args.uid:
                payload["uid"] = args.uid
            result = client.call_tool("take_screenshot", payload)
            print_json(result)
            if not has_tool_error(result):
                print(out_path)
                return 0
            return 1

        if args.command == "click":
            payload = {"uid": args.uid}
            if args.double:
                payload["dblClick"] = True
            result = client.call_tool("click", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "fill":
            result = client.call_tool("fill", {"uid": args.uid, "value": args.value})
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "press":
            result = client.call_tool("press_key", {"key": args.key})
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "wait":
            timeout_ms = normalize_timeout_ms(args.timeout, args.quiet, "wait") or DEFAULT_TIMEOUT_MS
            if args.text:
                payload = {"text": args.text, "timeout": timeout_ms}
                result = client.call_tool("wait_for", payload)
                print_json(result)
                return 1 if has_tool_error(result) else 0
            result = wait_for_ready_state(client, timeout_ms, args.quiet)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "list-pages":
            result = client.call_tool("list_pages", {})
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "select-page":
            payload = {"pageIdx": args.index}
            if args.bring_to_front:
                payload["bringToFront"] = True
            result = client.call_tool("select_page", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "close-page":
            result = client.call_tool("close_page", {"pageIdx": args.index})
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "list-console":
            payload: Dict[str, Any] = {}
            if args.page_idx is not None:
                payload["pageIdx"] = args.page_idx
            if args.page_size is not None:
                payload["pageSize"] = args.page_size
            if args.include_preserved:
                payload["includePreservedMessages"] = True
            if args.types:
                payload["types"] = args.types
            result = client.call_tool("list_console_messages", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "list-network":
            payload: Dict[str, Any] = {}
            if args.page_idx is not None:
                payload["pageIdx"] = args.page_idx
            if args.page_size is not None:
                payload["pageSize"] = args.page_size
            if args.include_preserved:
                payload["includePreservedRequests"] = True
            if args.resource_types:
                payload["resourceTypes"] = args.resource_types
            result = client.call_tool("list_network_requests", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "trace-start":
            payload = {"autoStop": args.auto_stop, "reload": args.reload}
            result = client.call_tool("performance_start_trace", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        if args.command == "trace-stop":
            result = client.call_tool("performance_stop_trace", {})
            out_path = args.out or default_output_path("trace", ".json")
            write_path = out_path
            if has_tool_error(result):
                base, ext = os.path.splitext(out_path)
                write_path = f"{base}_error{ext}"
            with open(write_path, "w", encoding="utf-8") as handle:
                json.dump(result, handle, ensure_ascii=False, indent=2)
            print_json(result)
            if has_tool_error(result):
                print(f"trace error output saved to {write_path}", file=sys.stderr)
                return 1
            print(write_path)
            return 0

        if args.command == "trace-insight":
            payload = {"insightName": args.name, "insightSetId": args.set_id}
            result = client.call_tool("performance_analyze_insight", payload)
            print_json(result)
            return 1 if has_tool_error(result) else 0

        raise RuntimeError(f"Unknown command: {args.command}")
    finally:
        client.close()


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run_command(args)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
