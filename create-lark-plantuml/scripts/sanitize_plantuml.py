#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 PlantUML 降级为更适配飞书画板的安全子集。

- 移除预处理/宏指令（如 !define / !include）
- 移除 skinparam 等样式指令
- 去除行首缩进（飞书画板粘贴更稳定）
- 清理类/接口成员可见性标记（+ - # ~）
- 清理常见颜色标记（#red / #EEEEEE 等）
- 可选保留 ArchiMate 的 !include 行
- 可选进入 ArchiMate 原生态模式（不做语法清理）
- 若缺失 @startuml/@enduml 则自动补齐

用法示例：
  python3 sanitize_plantuml.py input.puml --output fixed.puml --report report.txt
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import List, Tuple


_COLOR_TOKEN_RE = re.compile(r"\s+#([0-9A-Fa-f]{3,6}|[A-Za-z]+)\b")
_START_RE = re.compile(r"^@startuml\b", re.IGNORECASE)
_END_RE = re.compile(r"^@enduml\b", re.IGNORECASE)
_START_MINDMAP_RE = re.compile(r"^@startmindmap\b", re.IGNORECASE)
_END_MINDMAP_RE = re.compile(r"^@endmindmap\b", re.IGNORECASE)
_SKINPARAM_RE = re.compile(r"^\s*skinparam\b", re.IGNORECASE)
_PREPROCESSOR_RE = re.compile(r"^\s*!\w+")
_CLASS_BLOCK_START_RE = re.compile(r"^\s*(class|interface)\s+([^{]+)\s*\{", re.IGNORECASE)
_VISIBILITY_RE = re.compile(r"^(\s*)[+\-#~]\s*")
_L2R_RE = re.compile(r"^\s*left\s+to\s+right\s+direction\b", re.IGNORECASE)
_ARCHIMATE_RE = re.compile(r"\barchimate\b", re.IGNORECASE)
_ARCHIMATE_INCLUDE_RE = re.compile(r"^\s*!include\s+<archimate/", re.IGNORECASE)


def _read_text(path: str) -> str:
    """从文件或 stdin 读取文本。"""
    if path == "-":
        return sys.stdin.read()
    with open(path, "r", encoding="utf-8") as handle:
        return handle.read()


def _write_text(path: str, content: str) -> None:
    """写入文本到文件或 stdout。"""
    if path == "-":
        sys.stdout.write(content)
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def _is_comment_line(stripped: str) -> bool:
    """判断是否为注释行（不做降级处理）。"""
    return stripped.startswith("'") or stripped.startswith("/'")


def _sanitize_lines(
    lines: List[str], allow_archimate: bool, archimate_raw: bool
) -> Tuple[str, List[str]]:
    """按安全子集规则清理 PlantUML，返回修正文案和变更说明。"""
    output_lines: List[str] = []
    report: List[str] = []
    has_start = False
    has_end = False
    start_token = None
    end_token = None
    in_class_block = False
    indent_removed = False

    has_archimate = any(_ARCHIMATE_RE.search(line) for line in lines)
    allow_archimate = allow_archimate or has_archimate
    archimate_raw = archimate_raw or has_archimate

    for index, raw_line in enumerate(lines, start=1):
        line = raw_line.rstrip("\n")
        if line.startswith((" ", "\t")):
            line = line.lstrip()
            indent_removed = True
        stripped = line.strip()

        if in_class_block:
            if "}" in stripped:
                in_class_block = False
                output_lines.append(line)
                continue
            if not stripped or _is_comment_line(stripped):
                output_lines.append(line)
                continue
            if archimate_raw:
                output_lines.append(line)
                continue
            cleaned_line, count = _VISIBILITY_RE.subn(r"\1", line)
            if count > 0:
                report.append(f"移除成员可见性标记（第{index}行）：{stripped}")
            output_lines.append(cleaned_line)
            continue

        # 空行或注释行保持原样。
        if not stripped or _is_comment_line(stripped):
            output_lines.append(line)
            continue

        # 规范化 @startuml / @enduml / @startmindmap / @endmindmap。
        if _START_RE.match(stripped):
            has_start = True
            start_token = "@startuml"
            if stripped != "@startuml":
                report.append(f"规范化 @startuml（第{index}行）")
            output_lines.append("@startuml")
            continue
        if _END_RE.match(stripped):
            has_end = True
            end_token = "@enduml"
            if stripped != "@enduml":
                report.append(f"规范化 @enduml（第{index}行）")
            output_lines.append("@enduml")
            continue
        if _START_MINDMAP_RE.match(stripped):
            has_start = True
            start_token = "@startmindmap"
            if stripped != "@startmindmap":
                report.append(f"规范化 @startmindmap（第{index}行）")
            output_lines.append("@startmindmap")
            continue
        if _END_MINDMAP_RE.match(stripped):
            has_end = True
            end_token = "@endmindmap"
            if stripped != "@endmindmap":
                report.append(f"规范化 @endmindmap（第{index}行）")
            output_lines.append("@endmindmap")
            continue

        if not archimate_raw:
            # 移除预处理/宏指令。
            if _PREPROCESSOR_RE.match(line):
                if allow_archimate and _ARCHIMATE_INCLUDE_RE.match(line):
                    output_lines.append(line)
                    continue
                report.append(f"移除预处理指令（第{index}行）：{stripped}")
                continue

            # 移除 skinparam 等样式指令。
            if _SKINPARAM_RE.match(line):
                report.append(f"移除 skinparam（第{index}行）：{stripped}")
                continue

            # 移除方向控制指令（飞书画板可能不支持）。
            if _L2R_RE.match(line):
                report.append(f"移除方向指令（第{index}行）：{stripped}")
                continue

        # 进入类/接口成员块。
        class_match = _CLASS_BLOCK_START_RE.match(line)
        if class_match:
            output_lines.append(line)
            if "}" not in stripped:
                in_class_block = True
            continue

        if not archimate_raw:
            # 清理颜色标记，避免飞书画板忽略或降级。
            cleaned_line, count = _COLOR_TOKEN_RE.subn("", line)
            if count > 0:
                report.append(f"移除颜色标记（第{index}行）：{stripped}")
                line = cleaned_line

        output_lines.append(line)

    # 自动补齐必要的起止标记。
    if not has_start:
        output_lines.insert(0, "@startuml")
        report.append("补充 @startuml")
    if not has_end:
        if start_token == "@startmindmap" or end_token == "@endmindmap":
            output_lines.append("@endmindmap")
            report.append("补充 @endmindmap")
        else:
            output_lines.append("@enduml")
            report.append("补充 @enduml")

    if indent_removed:
        report.append("移除行首缩进")

    sanitized = "\n".join(output_lines).rstrip() + "\n"
    return sanitized, report


def _write_report(path: str, report: List[str]) -> None:
    """输出变更说明到文件或 stderr。"""
    if not report:
        return
    lines = ["变更说明:"] + [f"- {item}" for item in report]
    content = "\n".join(lines) + "\n"
    if path == "-":
        sys.stderr.write(content)
        return
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(content)


def main() -> int:
    parser = argparse.ArgumentParser(description="降级 PlantUML 为飞书安全子集")
    parser.add_argument("input", nargs="?", default="-", help="输入文件路径，默认为 stdin")
    parser.add_argument("--output", "-o", default="-", help="输出文件路径，默认为 stdout")
    parser.add_argument("--report", default="-", help="变更说明输出路径，默认写到 stderr")
    parser.add_argument("--allow-archimate", action="store_true", help="保留 ArchiMate 的 !include 行")
    parser.add_argument(
        "--archimate-raw",
        action="store_true",
        help="ArchiMate 原生态模式：不移除样式/颜色/方向/预处理，仅去缩进",
    )
    args = parser.parse_args()

    text = _read_text(args.input)
    lines = text.splitlines()
    sanitized, report = _sanitize_lines(lines, args.allow_archimate, args.archimate_raw)

    _write_text(args.output, sanitized)
    _write_report(args.report, report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
