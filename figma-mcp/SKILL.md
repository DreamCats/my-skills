---
name: figma-mcp
description: 通过 figma-developer-mcp（stdio）连接 Figma MCP，支持列出工具、调用工具、排查 MCP 交互问题；当需要在命令行与 Figma 文件/节点交互或调试 MCP 行为时使用。
---

# Figma MCP

## 快速开始

1. 进入技能目录再执行脚本：
   `cd /Users/bytedance/.codex/skills/figma-mcp`
2. 确认密钥文件：`~/.config/figma-mcp/.env`（内容示例：`key=xxx`）。
3. 列出工具：`python3 scripts/figma_mcp.py list-tools`
4. 调用工具：
   `python3 scripts/figma_mcp.py call --name <tool> --args '{"key":"value"}'`

## 配置与规则

- 默认从 `~/.config/figma-mcp/.env` 读取 `key=...`，也可通过 `FIGMA_API_KEY` 或 `--api-key` 覆盖。
- 脚本使用 stdio 协议启动：`npx -y figma-developer-mcp --figma-api-key=... --stdio`。
- 脚本会自动执行 `initialize` 与 `notifications/initialized`；如需跳过，使用 `--no-init`。

## 常用命令

- 列工具：`python3 scripts/figma_mcp.py list-tools --pretty`
- 调用工具：
  `python3 scripts/figma_mcp.py call --name <tool> --args-file /path/to/args.json`
- 调用自定义方法：
  `python3 scripts/figma_mcp.py rpc --method <method> --params '{"foo":"bar"}'`

## 脚本说明

- `scripts/figma_mcp.py`：标准 MCP stdio 客户端，负责握手、请求、输出结果。
- 遇到非 JSON 输出或启动日志会打印到 stderr，不影响主输出。

## 参考

- `references/examples.md`：常见调用示例与排查思路。
