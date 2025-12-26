#!/usr/bin/env python3
import argparse
import json
import os
import queue
import subprocess
import sys
import threading
import time

DEFAULT_ENV_PATH = os.path.expanduser("~/.config/figma-mcp/.env")
DEFAULT_PROTOCOL_VERSION = "2024-11-05"
DEFAULT_CLIENT_INFO = {"name": "figma-mcp-client", "version": "0.1.0"}


class StdioMCPClient:
    def __init__(self, cmd, timeout):
        self._cmd = cmd
        self._timeout = timeout
        self._proc = subprocess.Popen(
            cmd,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self._id = 0
        self._lock = threading.Lock()
        self._queue = queue.Queue()
        self._pending = {}
        self._closed = False

        self._stdout_thread = threading.Thread(
            target=self._read_stdout, args=(self._proc.stdout,), daemon=True
        )
        self._stderr_thread = threading.Thread(
            target=self._read_stderr, args=(self._proc.stderr,), daemon=True
        )
        self._stdout_thread.start()
        self._stderr_thread.start()

    def _read_stdout(self, stream):
        for raw in iter(stream.readline, ""):
            line = raw.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                print(f"[figma-mcp] stdout: {line}", file=sys.stderr)
                continue
            msg_id = msg.get("id")
            if msg_id is None:
                # Notification or server log in JSON.
                continue
            with self._lock:
                self._pending[msg_id] = msg
            self._queue.put(msg_id)
        self._closed = True

    def _read_stderr(self, stream):
        for raw in iter(stream.readline, ""):
            line = raw.rstrip()
            if line:
                print(f"[figma-mcp] {line}", file=sys.stderr)

    def _next_id(self):
        with self._lock:
            self._id += 1
            return self._id

    def _send(self, payload):
        if self._proc.stdin is None:
            raise RuntimeError("MCP process stdin not available")
        self._proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self._proc.stdin.flush()

    def notify(self, method, params=None):
        payload = {"jsonrpc": "2.0", "method": method}
        if params is not None:
            payload["params"] = params
        self._send(payload)

    def request(self, method, params=None):
        request_id = self._next_id()
        payload = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = params
        self._send(payload)
        return self._wait_for(request_id, self._timeout)

    def _wait_for(self, request_id, timeout):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with self._lock:
                if request_id in self._pending:
                    return self._pending.pop(request_id)
            try:
                self._queue.get(timeout=0.1)
            except queue.Empty:
                if self._closed:
                    break
                continue
        raise TimeoutError(f"Timed out waiting for response id={request_id}")

    def close(self):
        if self._proc.poll() is None:
            self._proc.terminate()
        try:
            self._proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            self._proc.kill()


def read_api_key(env_path):
    direct = os.getenv("FIGMA_API_KEY")
    if direct:
        return direct
    if not os.path.exists(env_path):
        return None
    key_map = {}
    with open(env_path, "r", encoding="utf-8") as handle:
        for raw in handle:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if "=" not in line:
                continue
            k, v = line.split("=", 1)
            key_map[k.strip().lower()] = v.strip()
    for candidate in ("figma_api_key", "key"):
        if candidate in key_map and key_map[candidate]:
            return key_map[candidate]
    return None


def build_command(npx_path, api_key):
    return [
        npx_path,
        "-y",
        "figma-developer-mcp",
        f"--figma-api-key={api_key}",
        "--stdio",
    ]


def load_json_arg(arg_text):
    if arg_text is None:
        return None
    return json.loads(arg_text)


def load_json_file(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def print_response(payload, pretty):
    if isinstance(payload, dict) and "error" in payload:
        print(json.dumps(payload["error"], ensure_ascii=False, indent=2 if pretty else None))
        return 1
    result = payload.get("result", payload)
    print(json.dumps(result, ensure_ascii=False, indent=2 if pretty else None))
    return 0


def run_command(args):
    api_key = args.api_key or read_api_key(args.env_file)
    if not api_key:
        raise SystemExit(
            "Missing Figma API key. Set FIGMA_API_KEY or add key=... in ~/.config/figma-mcp/.env"
        )

    cmd = build_command(args.npx, api_key)
    client = StdioMCPClient(cmd, args.timeout)
    try:
        if not args.no_init:
            init_payload = {
                "protocolVersion": DEFAULT_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": DEFAULT_CLIENT_INFO,
            }
            init_resp = client.request("initialize", init_payload)
            if "error" in init_resp:
                return print_response(init_resp, args.pretty)
            client.notify("notifications/initialized")

        if args.subcommand == "list-tools":
            resp = client.request("tools/list", {})
            return print_response(resp, args.pretty)

        if args.subcommand == "call":
            tool_args = None
            if args.args_file:
                tool_args = load_json_file(args.args_file)
            elif args.args:
                tool_args = load_json_arg(args.args)
            params = {"name": args.name, "arguments": tool_args or {}}
            resp = client.request("tools/call", params)
            return print_response(resp, args.pretty)

        if args.subcommand == "rpc":
            params = None
            if args.params_file:
                params = load_json_file(args.params_file)
            elif args.params:
                params = load_json_arg(args.params)
            resp = client.request(args.method, params)
            return print_response(resp, args.pretty)

        raise SystemExit("Unknown command")
    finally:
        client.close()


def build_parser():
    parser = argparse.ArgumentParser(
        description="Figma MCP stdio client for figma-developer-mcp"
    )
    parser.add_argument(
        "--env-file",
        default=DEFAULT_ENV_PATH,
        help="Path to env file (default: ~/.config/figma-mcp/.env)",
    )
    parser.add_argument(
        "--api-key",
        help="Override Figma API key (or use FIGMA_API_KEY env)",
    )
    parser.add_argument("--npx", default="npx", help="npx path")
    parser.add_argument(
        "--timeout",
        type=int,
        default=60,
        help="Request timeout in seconds",
    )
    parser.add_argument("--no-init", action="store_true", help="Skip initialize")
    parser.add_argument("--pretty", action="store_true", help="Pretty JSON output")

    pretty_parent = argparse.ArgumentParser(add_help=False)
    pretty_parent.add_argument(
        "--pretty", action="store_true", help="Pretty JSON output"
    )

    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    list_parser = subparsers.add_parser(
        "list-tools", help="List MCP tools", parents=[pretty_parent]
    )
    list_parser.set_defaults(func=run_command)

    call_parser = subparsers.add_parser(
        "call", help="Call MCP tool", parents=[pretty_parent]
    )
    call_parser.add_argument("--name", required=True, help="Tool name")
    call_parser.add_argument("--args", help="Tool args JSON string")
    call_parser.add_argument("--args-file", help="Tool args JSON file")
    call_parser.set_defaults(func=run_command)

    rpc_parser = subparsers.add_parser(
        "rpc", help="Call arbitrary MCP method", parents=[pretty_parent]
    )
    rpc_parser.add_argument("--method", required=True, help="JSON-RPC method")
    rpc_parser.add_argument("--params", help="Params JSON string")
    rpc_parser.add_argument("--params-file", help="Params JSON file")
    rpc_parser.set_defaults(func=run_command)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        exit_code = args.func(args)
    except TimeoutError as exc:
        print(f"Timeout: {exc}", file=sys.stderr)
        exit_code = 2
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON: {exc}", file=sys.stderr)
        exit_code = 2
    except KeyboardInterrupt:
        exit_code = 130
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
