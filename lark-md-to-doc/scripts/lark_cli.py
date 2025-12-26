"""
lark-cli 调用与输出解析。
"""

import json
import subprocess
import sys


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
    """启发式判断 doc id。"""
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
