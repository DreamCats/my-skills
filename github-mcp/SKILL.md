---
name: github-mcp
description: Use when Codex needs to operate GitHub via an MCP server over HTTP, including creating/updating files, pushing multiple files, searching repositories/code/issues/users, creating issues/PRs, listing commits/PRs, reviewing/merging PRs, or other GitHub MCP tool calls.
---

# GitHub MCP (HTTP)

Use the HTTP MCP server to run GitHub operations through tool calls. Prefer the bundled script so the protocol details stay consistent.

## Quick start

Run commands from the skill directory so relative paths resolve:

```bash
# 先进入技能命令在执行
cd xxx/skills/github-mcp
```

1. Use the default MCP endpoint (URL already includes the token), or override if needed:

```bash
# Default URL is baked into the script:
# https://mcp.api-inference.modelscope.net/3da3158cbc1a4b/mcp
# Optional override:
export GITHUB_MCP_URL="https://mcp.api-inference.modelscope.net/3da3158cbc1a4b/mcp"
```

2. List tools:

```bash
python3 scripts/github_mcp.py list-tools
```

3. Call a tool:

```bash
python3 scripts/github_mcp.py call \
  --name create_issue \
  --args '{"owner":"octo","repo":"demo","title":"Bug","body":"Steps..."}'
```

## Workflow

- Confirm the MCP base URL and auth header requirements for your server (this default URL already embeds the token).
- Run `list-tools` to confirm the tool names available.
- Build the JSON args for the tool; use `get_file_contents` to fetch `sha` before updates.
- Prefer `push_files` when committing multiple files in one change.
- Use `rpc` if your MCP server exposes non-standard method names.
- Review responses for `error` and stop on failures.

## Tool reference

See `references/github_tools.md` for the available tool list and search query syntax.

## Notes

- The script speaks JSON-RPC over HTTP. For streamable_http servers, it sends `Accept: application/json, text/event-stream`.
- For streamable_http servers that require session headers, the script captures `mcp-session-id` from `initialize` and reuses it automatically.
- The script sends `notifications/initialized` after `initialize` to satisfy servers that require the post-init handshake.
- If your server uses a different endpoint or headers, pass `--url` and `--header`.
- Output is a JSON response; check `result` for tool output and commit details.
