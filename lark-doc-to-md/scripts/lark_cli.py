import json
import subprocess
import sys


def run_cmd(cmd, quiet=True):
    proc = subprocess.run(cmd, text=True, capture_output=True)
    if proc.returncode == 0:
        return proc.stdout
    output = (proc.stdout or "") + (proc.stderr or "")
    if quiet and "41050" in output:
        return ""
    if not quiet:
        sys.stderr.write(proc.stdout or "")
        sys.stderr.write(proc.stderr or "")
        sys.stderr.write(f"Command failed: {' '.join(cmd)}\n")
    raise subprocess.CalledProcessError(
        proc.returncode, cmd, output=proc.stdout, stderr=proc.stderr
    )


def resolve_wiki_node(node_token):
    raw = run_cmd(["lark-cli", "--format", "json", "get-node", node_token])
    if not raw:
        return ""
    data = json.loads(raw)
    obj_token = data.get("obj_token")
    if not obj_token:
        raise ValueError(f"get-node missing obj_token for wiki token: {node_token}")
    return obj_token


def get_blocks(doc_id):
    raw = run_cmd(["lark-cli", "--format", "json", "get-blocks", doc_id, "--all"])
    if not raw:
        return {"items": []}
    return json.loads(raw)


def get_user_info(user_id, user_id_type="user_id"):
    raw = run_cmd(
        ["lark-cli", "--format", "json", "get-user-info", user_id, "--user-id-type", user_id_type]
    )
    if not raw:
        return {}
    return json.loads(raw)
