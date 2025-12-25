import json
import subprocess
import sys


def run_cmd(cmd):
    try:
        return subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError as exc:
        sys.stderr.write(exc.stdout or "")
        sys.stderr.write(exc.stderr or "")
        sys.stderr.write(f"Command failed: {' '.join(cmd)}\n")
        raise


def resolve_wiki_node(node_token):
    raw = run_cmd(["lark-cli", "--format", "json", "get-node", node_token])
    data = json.loads(raw)
    obj_token = data.get("obj_token")
    if not obj_token:
        raise ValueError(f"get-node missing obj_token for wiki token: {node_token}")
    return obj_token


def get_blocks(doc_id):
    raw = run_cmd(["lark-cli", "--format", "json", "get-blocks", doc_id, "--all"])
    return json.loads(raw)


def get_user_info(user_id, user_id_type="user_id"):
    raw = run_cmd(
        ["lark-cli", "--format", "json", "get-user-info", user_id, "--user-id-type", user_id_type]
    )
    return json.loads(raw)
