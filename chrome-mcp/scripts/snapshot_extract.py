#!/usr/bin/env python3
"""Extract actionable element uids from a chrome-devtools-mcp snapshot."""

import argparse
import re
import sys
from typing import Iterable, List, Optional, Tuple

UID_RE = re.compile(r"\buid\s*[:=]\s*([A-Za-z0-9_-]+)")
ROLE_RE = re.compile(r"\brole\s*[:=]\s*([A-Za-z0-9_-]+)")
LABEL_RE = re.compile(r"\b(name|text|label|value)\s*[:=]\s*(\"[^\"]*\"|'[^']*'|\S+)")

INTERACTIVE_ROLES = {
    "button",
    "link",
    "textbox",
    "input",
    "combobox",
    "listbox",
    "menuitem",
    "checkbox",
    "radio",
    "option",
    "tab",
    "switch",
}


def _read_text(path: str) -> str:
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def _clean_value(raw: str) -> str:
    if len(raw) >= 2 and ((raw[0] == '"' and raw[-1] == '"') or (raw[0] == "'" and raw[-1] == "'")):
        return raw[1:-1]
    return raw


def _parse_line(line: str) -> Optional[Tuple[str, str, str, str]]:
    uid_match = UID_RE.search(line)
    if not uid_match:
        return None
    uid = uid_match.group(1)

    role_match = ROLE_RE.search(line)
    role = role_match.group(1).lower() if role_match else ""

    label_match = LABEL_RE.search(line)
    label = _clean_value(label_match.group(2)) if label_match else ""

    return uid, role, label, line.strip()


def _filter_records(
    records: Iterable[Tuple[str, str, str, str]],
    only_roles: Optional[List[str]],
    show_all: bool,
) -> List[Tuple[str, str, str, str]]:
    normalized_roles = {role.lower() for role in only_roles} if only_roles else set()
    results: List[Tuple[str, str, str, str]] = []
    for uid, role, label, raw in records:
        if normalized_roles and role not in normalized_roles:
            continue
        if not show_all and not normalized_roles and role and role not in INTERACTIVE_ROLES:
            continue
        results.append((uid, role, label, raw))
    return results


def extract_records(text: str) -> List[Tuple[str, str, str, str]]:
    records = []
    for line in text.splitlines():
        if "uid" not in line:
            continue
        parsed = _parse_line(line)
        if parsed:
            records.append(parsed)
    return records


def render_records(records: List[Tuple[str, str, str, str]], max_items: int) -> str:
    lines = []
    for idx, (uid, role, label, raw) in enumerate(records):
        if max_items and idx >= max_items:
            break
        if role or label:
            lines.append(f"uid={uid}\trole={role or '-'}\tlabel={label or '-'}")
        else:
            lines.append(f"uid={uid}\t{raw}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Extract element uids from chrome-devtools-mcp snapshots."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Snapshot file path. Use '-' to read from stdin.",
    )
    parser.add_argument(
        "--show-all",
        action="store_true",
        help="Show all elements containing uid, not only interactive roles.",
    )
    parser.add_argument(
        "--only-roles",
        help="Comma-separated roles to keep (overrides default filter).",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=0,
        help="Limit output count. 0 means no limit.",
    )
    args = parser.parse_args()

    text = _read_text(args.input)
    records = extract_records(text)
    only_roles = [role.strip() for role in args.only_roles.split(",")] if args.only_roles else None
    filtered = _filter_records(records, only_roles, args.show_all)

    if not filtered and records:
        filtered = records

    output = render_records(filtered, args.max)
    if output:
        print(output)
        return 0

    print("No uid entries found.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
