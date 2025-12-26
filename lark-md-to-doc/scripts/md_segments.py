"""
Markdown 分段解析。
"""

import shlex


def parse_callout_info(info_line):
    """解析 callout 指令参数。

    支持：
    - ```callout type=warning
    - ```callout:warning
    """
    opts = {}
    # 用 shlex 处理引号与空格，避免手写分词的坑
    tokens = shlex.split(info_line)
    if tokens:
        head = tokens[0]
        if ":" in head:
            _, val = head.split(":", 1)
            if val:
                opts["type"] = val
        for token in tokens[1:]:
            if "=" in token:
                key, value = token.split("=", 1)
                if key.lower() in ("type", "callout-type"):
                    opts[key.lower()] = value
    if "callout-type" in opts and "type" not in opts:
        opts["type"] = opts["callout-type"]
    return opts


def parse_segments(markdown_text):
    """将 Markdown 分割为三类片段：

    - ("markdown", text)
    - ("callout", info_line, text)
    - ("diagram", syntax, text)
    """
    lines = markdown_text.splitlines()
    segments = []
    buf = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            info = line.strip()[3:].strip()
            info_lower = info.lower()
            is_callout = info_lower.startswith("callout")
            is_plantuml = info_lower.startswith("plantuml")
            is_mermaid = info_lower.startswith("mermaid")
            if is_callout or is_plantuml or is_mermaid:
                # 进入指令块，先把之前的普通 Markdown 缓冲输出
                if buf:
                    segments.append(("markdown", "\n".join(buf)))
                    buf = []
                i += 1
                block_lines = []
                while i < len(lines) and not lines[i].startswith("```"):
                    block_lines.append(lines[i])
                    i += 1
                block_text = "\n".join(block_lines)
                if is_callout:
                    segments.append(("callout", info, block_text))
                else:
                    syntax = "plantuml" if is_plantuml else "mermaid"
                    segments.append(("diagram", syntax, block_text))
            else:
                # 非指令块的代码块，按原样写入 Markdown
                buf.append(line)
                i += 1
                while i < len(lines):
                    buf.append(lines[i])
                    if lines[i].startswith("```"):
                        break
                    i += 1
        else:
            buf.append(line)
        i += 1
    if buf:
        segments.append(("markdown", "\n".join(buf)))
    return segments
