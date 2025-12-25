#!/usr/bin/env python3
"""
将 Markdown 渲染到飞书云文档：
- 普通 Markdown 段落：lark-cli add-content
- ```plantuml / ```mermaid：创建画板并导入图表
- ```callout：创建高亮块

输入：Markdown 文件
输出：写入到指定/新建的飞书文档
"""

import argparse
import json
import os
import shlex
import subprocess
import sys
import tempfile


def run_lark_cli(args, want_json=False, verbose=False):
    """执行 lark-cli 命令。

    - want_json=True 时解析 JSON 输出
    - verbose=True 时添加 -v
    - 失败时直接退出并输出错误信息
    """
    cmd = ["lark-cli"]
    # JSON 输出需要保持纯净，避免 -v 混入日志导致解析失败
    if verbose and not want_json:
        cmd.append("-v")
    if want_json:
        cmd += ["--format", "json"]
    cmd += args
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        # lark-cli 可能将错误写到 stdout 或 stderr，这里统一输出
        sys.stderr.write(res.stderr or res.stdout)
        raise SystemExit(res.returncode)
    if want_json:
        try:
            return json.loads(res.stdout)
        except json.JSONDecodeError:
            # JSON 解析失败时，直接输出原始文本便于排查
            sys.stderr.write(res.stdout)
            raise SystemExit(2)
    return res.stdout


def extract_id(data, keys, value_predicate=None):
    """从任意层级 JSON 中提取 id。

    - keys：可能的字段名列表
    - value_predicate：用于验证 id 是否符合预期格式
    """
    if isinstance(data, dict):
        for key in keys:
            if key in data and isinstance(data[key], str):
                if value_predicate is None or value_predicate(data[key]):
                    return data[key]
        for value in data.values():
            found = extract_id(value, keys, value_predicate)
            if found:
                return found
    elif isinstance(data, list):
        for value in data:
            found = extract_id(value, keys, value_predicate)
            if found:
                return found
    return None


def is_doc_id(value):
    """启发式判断 doc id。

    飞书文档 token 不一定以 docx 开头，这里放宽判断：
    - 非空字符串且长度看起来合理
    """
    if not isinstance(value, str):
        return False
    v = value.strip()
    return len(v) >= 8


def is_board_id(value):
    """启发式判断 whiteboard/board id。"""
    if not isinstance(value, str):
        return False
    v = value.strip()
    return len(v) >= 8


def create_document(title, folder_token, verbose=False):
    """创建文档并返回 doc_id。"""
    args = ["create-document", "--title", title]
    if folder_token:
        args += ["--folder-token", folder_token]
    data = run_lark_cli(args, want_json=True, verbose=verbose)
    # 优先从明确字段读取，避免被其他 token 干扰
    doc_id = extract_id(
        data,
        [
            "document_id",
            "doc_id",
            "docx_token",
            "docxToken",
            "documentId",
            "docId",
        ],
    )
    # 兼容结构不一致的情况，再尝试宽松匹配
    if not doc_id:
        doc_id = extract_id(
            data,
            ["token", "id"],
            value_predicate=is_doc_id,
        )
    if not doc_id:
        sys.stderr.write("Failed to parse document id from create-document output.\n")
        raise SystemExit(3)
    # 尝试直接取 url（如存在）
    doc_url = None
    if isinstance(data, dict):
        url = data.get("url")
        if isinstance(url, str) and url.strip():
            doc_url = url.strip()
    return doc_id, doc_url


def add_markdown(doc_id, text, verbose=False):
    """将一段 Markdown 写入文档。"""
    if not text.strip():
        return
    # 使用临时文件，避免命令行长度限制和转义问题
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".md", encoding="utf-8") as tmp:
        tmp.write(text)
        tmp_path = tmp.name
    try:
        run_lark_cli(["add-content", doc_id, tmp_path], want_json=False, verbose=verbose)
    finally:
        os.unlink(tmp_path)


def add_callout(doc_id, text, callout_type=None, verbose=False):
    """创建高亮块。"""
    if not text.strip():
        return
    args = ["add-callout", doc_id, text]
    if callout_type:
        args += ["--callout-type", callout_type]
    run_lark_cli(args, want_json=False, verbose=verbose)


def add_board(doc_id, verbose=False):
    """创建画板并返回 whiteboard_id。"""
    data = run_lark_cli(["add-board", doc_id], want_json=True, verbose=verbose)
    # 先从标准结构里取 board.token
    board_id = None
    if isinstance(data, dict):
        children = data.get("children")
        if isinstance(children, list):
            for child in children:
                if isinstance(child, dict):
                    board = child.get("board")
                    if isinstance(board, dict):
                        token = board.get("token")
                        if isinstance(token, str) and token.strip():
                            board_id = token.strip()
                            break
    if not board_id:
        board_id = extract_id(
            data,
            ["whiteboard_id", "whiteboardId", "board_id", "boardId", "token", "id"],
            value_predicate=is_board_id,
        )
    if not board_id:
        sys.stderr.write("Failed to parse whiteboard id from add-board output.\n")
        raise SystemExit(4)
    return board_id


def import_diagram(board_id, content, syntax, verbose=False):
    """导入图表到画板。

    syntax：plantuml 或 mermaid
    """
    if not content.strip():
        return
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".puml", encoding="utf-8") as tmp:
        tmp.write(content)
        tmp_path = tmp.name
    try:
        run_lark_cli(
            [
                "import-diagram",
                board_id,
                tmp_path,
                "--source-type",
                "file",
                "--syntax",
                syntax,
            ],
            want_json=False,
            verbose=verbose,
        )
    finally:
        os.unlink(tmp_path)


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


def main():
    parser = argparse.ArgumentParser(description="Render Markdown into Lark doc with lark-cli.")
    parser.add_argument("--md", required=True, help="Markdown file to render")
    parser.add_argument("--doc-id", help="Existing Lark doc id")
    parser.add_argument("--title", help="Create a new document with title")
    parser.add_argument("--folder-token", help="Optional folder token for new doc")
    parser.add_argument("--dry-run", action="store_true", help="Print steps without calling lark-cli")
    parser.add_argument("--verbose", action="store_true", help="Verbose lark-cli output")
    args = parser.parse_args()

    if not args.doc_id and not args.title:
        parser.error("Either --doc-id or --title is required")

    with open(args.md, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    # 创建或复用文档
    doc_id = args.doc_id
    doc_url = None
    if not doc_id:
        if args.dry_run:
            # dry-run 不调用 lark-cli，用占位符代替
            doc_id = "DOC_ID"
        else:
            doc_id, doc_url = create_document(args.title, args.folder_token, verbose=args.verbose)
            # 默认输出 doc_id 与 url，方便用户回收链接
            print(f"doc_id: {doc_id}")
            if doc_url:
                print(f"url: {doc_url}")

    # 解析 Markdown 为可执行片段
    segments = parse_segments(markdown_text)

    # 按顺序渲染到文档
    for segment in segments:
        kind = segment[0]
        if kind == "markdown":
            if args.dry_run:
                print("[markdown]", (segment[1][:80] + "...") if len(segment[1]) > 80 else segment[1])
            else:
                add_markdown(doc_id, segment[1], verbose=args.verbose)
        elif kind == "callout":
            info_line, text = segment[1], segment[2]
            opts = parse_callout_info(info_line)
            if args.dry_run:
                print("[callout]", opts, (text[:80] + "...") if len(text) > 80 else text)
            else:
                add_callout(
                    doc_id,
                    text.strip(),
                    callout_type=opts.get("type"),
                    verbose=args.verbose,
                )
        elif kind == "diagram":
            syntax, text = segment[1], segment[2]
            if args.dry_run:
                print(f"[diagram:{syntax}]", (text[:80] + "...") if len(text) > 80 else text)
            else:
                board_id = add_board(doc_id, verbose=args.verbose)
                import_diagram(board_id, text.strip(), syntax=syntax, verbose=args.verbose)
        else:
            raise SystemExit(f"Unknown segment type: {kind}")


if __name__ == "__main__":
    main()
