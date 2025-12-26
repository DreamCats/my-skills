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

from lark_doc_ops import add_board, add_callout, add_markdown, create_document, import_diagram
from md_segments import parse_callout_info, parse_segments


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
