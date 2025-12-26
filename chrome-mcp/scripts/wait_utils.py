from __future__ import annotations

import json
import re
import time
import sys
from typing import Any, Dict, Optional

from config import has_tool_error
from mcp_client import MCPClient


def extract_json_from_text(text: str) -> Optional[Any]:
    match = re.search(r"```json\\n(.*?)\\n```", text, re.DOTALL)
    if not match:
        return None
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return None


def extract_eval_result(result: Dict[str, Any]) -> Optional[Any]:
    for item in result.get("content", []):
        if item.get("type") != "text":
            continue
        payload = extract_json_from_text(item.get("text", ""))
        if payload is not None:
            return payload
    return None


def wait_for_ready_state(client: MCPClient, timeout_ms: int, quiet: bool) -> Dict[str, Any]:
    deadline = time.monotonic() + (timeout_ms / 1000)
    last_state: Optional[str] = None
    while time.monotonic() <= deadline:
        result = client.call_tool("evaluate_script", {"function": "() => document.readyState"})
        if has_tool_error(result):
            return result
        payload = extract_eval_result(result)
        if isinstance(payload, str):
            last_state = payload
            if payload == "complete":
                return {
                    "content": [
                        {"type": "text", "text": "Document readyState reached 'complete'."}
                    ]
                }
        time.sleep(0.5)
    if not quiet:
        print(
            "Timeout waiting for document.readyState to be 'complete'.",
            file=sys.stderr,
        )
    return {
        "content": [
            {
                "type": "text",
                "text": (
                    f"Timeout {timeout_ms} ms waiting for document.readyState "
                    f"to be 'complete'. Last state: {last_state or 'unknown'}."
                ),
            }
        ],
        "isError": True,
    }
