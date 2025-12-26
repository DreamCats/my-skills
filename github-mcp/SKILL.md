---
name: github-mcp
description: 当需要通过 HTTP 的 MCP 服务操作 GitHub（如创建/更新文件、批量提交、搜索仓库/代码/问题/用户、创建/查询/更新 Issue 与 PR、查看提交、审查与合并 PR 等）时使用。
---

# GitHub MCP（HTTP）

通过 HTTP MCP 服务器调用 GitHub 工具。优先使用脚本，保证协议细节一致。

## 快速开始

先进入技能目录，避免相对路径问题：

```bash
cd /Users/bytedance/.codex/skills/github-mcp
```

1. 使用默认 MCP 入口（URL 已内置 token），必要时可覆盖：

```bash
# 脚本内置默认 URL：
# https://mcp.api-inference.modelscope.net/3da3158cbc1a4b/mcp
# 可选覆盖：
export GITHUB_MCP_URL="https://mcp.api-inference.modelscope.net/3da3158cbc1a4b/mcp"
```

2. 列出工具列表：

```bash
python3 scripts/github_mcp.py list-tools
```

3. 调用工具：

```bash
python3 scripts/github_mcp.py call \
  --name create_issue \
  --args '{"owner":"octo","repo":"demo","title":"Bug","body":"Steps..."}'
```

## 工作流

- 确认 MCP 服务入口与鉴权要求（该默认 URL 已内置 token）。
- 先用 `list-tools` 验证可用的工具名。
- 按工具定义构造 JSON 参数；更新文件前先用 `get_file_contents` 拿到 `sha`。
- 多文件一次提交优先用 `push_files`。
- 若 MCP 服务方法名不标准，可用 `rpc` 直调。
- 响应里若有 `error`，立即停止并排查。

## 工具参考

工具清单与搜索语法见 `references/github_tools.md`。

## 备注

- 脚本使用 JSON-RPC over HTTP。streamable_http 服务需带 `Accept: application/json, text/event-stream`，脚本已默认发送。
- 对需要 session 的服务，脚本会在 `initialize` 后自动读取并复用 `mcp-session-id`。
- 脚本会在 `initialize` 后发送 `notifications/initialized` 以完成握手。
- 若服务端入口或 header 不同，可用 `--url` 和 `--header` 覆盖。
- Output is a JSON response; check `result` for tool output and commit details.
