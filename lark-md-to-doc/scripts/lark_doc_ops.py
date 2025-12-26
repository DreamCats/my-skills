"""
飞书文档写入相关操作。
"""

import os
import sys
import tempfile

from lark_cli import extract_id, is_board_id, is_doc_id, run_lark_cli


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
    """导入图表到画板。"""
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
