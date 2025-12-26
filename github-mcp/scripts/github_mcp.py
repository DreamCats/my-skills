#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.request

DEFAULT_PROTOCOL_VERSION = "2024-11-05"
DEFAULT_TIMEOUT = 60
DEFAULT_URL = "https://mcp.api-inference.modelscope.net/3da3158cbc1a4b/mcp"


def eprint(message: str) -> None:
    print(message, file=sys.stderr)


def load_json_from_arg(value: str) -> object:
    try:
        return json.loads(value)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON: {exc}") from exc


def load_json_from_file(path: str) -> object:
    with open(path, "r", encoding="utf-8") as handle:
        return load_json_from_arg(handle.read())


def parse_headers(header_list, token):
    headers = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream"}
    lower_keys = set()
    for item in header_list or []:
        if ":" not in item:
            raise ValueError(f"Header must be 'Key: Value', got: {item}")
        key, value = item.split(":", 1)
        key = key.strip()
        value = value.strip()
        headers[key] = value
        lower_keys.add(key.lower())
    if token and "authorization" not in lower_keys:
        headers["Authorization"] = f"Bearer {token}"
    return headers


class MCPClient:
    def __init__(self, url: str, headers: dict, timeout: int):
        self.url = url
        self.headers = headers
        self.timeout = timeout
        self._request_id = 1
        self.session_id = None

    def _request(self, method: str, params: object | None):
        payload = {
            "jsonrpc": "2.0",
            "id": self._request_id,
            "method": method,
        }
        if params is not None:
            payload["params"] = params
        self._request_id += 1
        data = json.dumps(payload).encode("utf-8")
        request_headers = dict(self.headers)
        if self.session_id and method != "initialize":
            request_headers["mcp-session-id"] = self.session_id
        req = urllib.request.Request(self.url, data=data, headers=request_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
                if method == "initialize":
                    header_session = resp.headers.get("mcp-session-id")
                    if header_session:
                        self.session_id = header_session.strip()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8") if exc.fp else ""
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Connection failed: {exc}") from exc
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Non-JSON response: {body}") from exc
        if method == "initialize" and not self.session_id:
            result = payload.get("result") if isinstance(payload, dict) else None
            if isinstance(result, dict):
                for key in ("session_id", "sessionId", "mcp_session_id"):
                    value = result.get(key)
                    if value:
                        self.session_id = str(value)
                        break
        return payload

    def _notify(self, method: str, params: object | None):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
        }
        if params is not None:
            payload["params"] = params
        data = json.dumps(payload).encode("utf-8")
        request_headers = dict(self.headers)
        if self.session_id:
            request_headers["mcp-session-id"] = self.session_id
        req = urllib.request.Request(self.url, data=data, headers=request_headers, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8") if exc.fp else ""
            raise RuntimeError(f"HTTP {exc.code}: {detail}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"Connection failed: {exc}") from exc
        if not body:
            return {}
        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Non-JSON response: {body}") from exc

    def initialize(self):
        params = {
            "protocolVersion": DEFAULT_PROTOCOL_VERSION,
            "clientInfo": {"name": "github-mcp-client", "version": "0.1"},
            "capabilities": {},
        }
        return self._request("initialize", params)

    def notify_initialized(self):
        return self._notify("notifications/initialized", {})

    def list_tools(self, cursor: str | None):
        if cursor is not None:
            return self._request("tools/list", {"cursor": cursor})
        param_variants = [
            {"cursor": ""},
            {"cursor": None},
            {},
            None,
        ]
        last_resp = None
        for params in param_variants:
            last_resp = self._request("tools/list", params)
            if not _is_param_error(last_resp):
                return last_resp
        return last_resp

    def call_tool(self, name: str, arguments: object):
        return self._request("tools/call", {"name": name, "arguments": arguments})

    def rpc(self, method: str, params: object | None):
        return self._request(method, params)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="GitHub MCP HTTP client")
    parser.add_argument("--url", default=os.environ.get("GITHUB_MCP_URL", DEFAULT_URL))
    parser.add_argument("--token", default=os.environ.get("GITHUB_MCP_TOKEN") or os.environ.get("GITHUB_TOKEN"))
    parser.add_argument("--header", action="append", default=[], help="Custom header: 'Key: Value'")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    parser.add_argument("--no-init", action="store_true", help="Skip initialize call")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print JSON")

    subparsers = parser.add_subparsers(dest="command", required=True)

    list_parser = subparsers.add_parser("list-tools")
    list_parser.add_argument("--cursor")

    call_parser = subparsers.add_parser("call")
    call_parser.add_argument("--name", required=True)
    call_parser.add_argument("--args")
    call_parser.add_argument("--args-file")

    rpc_parser = subparsers.add_parser("rpc")
    rpc_parser.add_argument("--method", required=True)
    rpc_parser.add_argument("--params")
    rpc_parser.add_argument("--params-file")

    return parser


def resolve_json_arg(value: str | None, file_path: str | None):
    if value and file_path:
        raise ValueError("Use either --args/--params or --args-file/--params-file, not both")
    if file_path:
        return load_json_from_file(file_path)
    if value:
        return load_json_from_arg(value)
    return {}


def print_json(data, pretty: bool):
    if pretty:
        print(json.dumps(data, ensure_ascii=True, indent=2, sort_keys=True))
    else:
        print(json.dumps(data, ensure_ascii=True))


def _is_param_error(response: object) -> bool:
    if not isinstance(response, dict):
        return False
    error = response.get("error")
    if not isinstance(error, dict):
        return False
    return error.get("code") == -32602


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.url:
        eprint("Missing --url or GITHUB_MCP_URL")
        return 2

    try:
        headers = parse_headers(args.header, args.token)
    except ValueError as exc:
        eprint(str(exc))
        return 2

    client = MCPClient(args.url, headers, args.timeout)

    if not args.no_init:
        try:
            init_resp = client.initialize()
            if "error" in init_resp:
                eprint(f"Initialize error: {init_resp['error']}")
                return 1
            init_notice = client.notify_initialized()
            if isinstance(init_notice, dict) and init_notice.get("error"):
                eprint(f"Initialize notification error: {init_notice['error']}")
                return 1
        except RuntimeError as exc:
            eprint(str(exc))
            return 1

    try:
        if args.command == "list-tools":
            resp = client.list_tools(args.cursor)
        elif args.command == "call":
            tool_args = resolve_json_arg(args.args, args.args_file)
            resp = client.call_tool(args.name, tool_args)
        elif args.command == "rpc":
            params = None if (args.params is None and args.params_file is None) else resolve_json_arg(args.params, args.params_file)
            resp = client.rpc(args.method, params)
        else:
            parser.error(f"Unknown command: {args.command}")
            return 2
    except (ValueError, RuntimeError) as exc:
        eprint(str(exc))
        return 1

    print_json(resp, args.pretty)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
