from __future__ import annotations

import json
import subprocess
import sys
from typing import Any, Dict, List, Optional

from config import DEFAULT_PROTOCOL_VERSION


class MCPClient:
    def __init__(self, command: str, args: List[str], protocol_version: str) -> None:
        self.command = command
        self.args = args
        self.protocol_version = protocol_version or DEFAULT_PROTOCOL_VERSION
        self.proc: Optional[subprocess.Popen[str]] = None
        self._next_id = 1

    def start(self) -> None:
        self.proc = subprocess.Popen(
            [self.command] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=sys.stderr,
            text=True,
            bufsize=1,
        )
        if not self.proc.stdin or not self.proc.stdout:
            raise RuntimeError("Failed to start MCP server process")

    def close(self) -> None:
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.proc.kill()

    def _send(self, payload: Dict[str, Any]) -> None:
        if not self.proc or not self.proc.stdin:
            raise RuntimeError("MCP server not running")
        self.proc.stdin.write(json.dumps(payload, ensure_ascii=False) + "\n")
        self.proc.stdin.flush()

    def _read_message(self) -> Optional[Dict[str, Any]]:
        if not self.proc or not self.proc.stdout:
            raise RuntimeError("MCP server not running")
        while True:
            line = self.proc.stdout.readline()
            if line == "":
                return None
            line = line.strip()
            if not line:
                continue
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue

    def request(self, method: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        request_id = self._next_id
        self._next_id += 1
        payload: Dict[str, Any] = {"jsonrpc": "2.0", "id": request_id, "method": method}
        if params is not None:
            payload["params"] = params
        self._send(payload)
        while True:
            msg = self._read_message()
            if msg is None:
                raise RuntimeError("MCP server closed unexpectedly")
            if msg.get("id") == request_id:
                if "error" in msg:
                    raise RuntimeError(f"MCP error: {msg['error']}")
                return msg.get("result", {})

    def initialize(self) -> Dict[str, Any]:
        params = {
            "protocolVersion": self.protocol_version,
            "clientInfo": {"name": "chrome-mcp-cli", "version": "0.1"},
            "capabilities": {},
        }
        result = self.request("initialize", params)
        self._send({"jsonrpc": "2.0", "method": "initialized", "params": {}})
        return result

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
        return self.request("tools/call", {"name": name, "arguments": arguments})

    def list_tools(self) -> Dict[str, Any]:
        return self.request("tools/list")
