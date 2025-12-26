---
name: chrome-mcp
description: 使用 Python3 作为 MCP Client 直接拉起并连接 chrome-devtools-mcp 控制 Chrome 浏览器，用于网页自动化、调试、性能分析、截图/快照、表单填充等任务；当用户需要在浏览器中执行步骤或获取页面信息时使用。
---

# Chrome MCP

## 概览

用 Python3 脚本作为 MCP Client，直接拉起 `chrome-devtools-mcp` 并控制 Chrome DevTools，完成页面访问、表单操作、截图/快照、网络与性能诊断等工作。

## 快速开始（Python3 脚本）

```bash
# 先进入技能目录
cd xxx/skills/chrome-mcp

# 打开页面并截图（默认先尝试连接已开启的 9222 调试端口）
python3 scripts/chrome_mcp.py navigate --url https://example.com
python3 scripts/chrome_mcp.py screenshot --full-page
```

默认行为：
- 优先连接 `http://127.0.0.1:9222`（若可用）。
- 若未发现可用调试端口，则自动启动一个新的 Chrome。
- 默认使用 `~/.chrome_mcp/chrome-profile` 作为浏览器数据目录，后续会自动复用该实例（避免重复启动报错）。
- 截图/快照/trace 默认输出到 `~/.chrome_mcp/logs/`。
- `new-page` / `navigate` / `wait` 默认超时 120s，可用 `--timeout` 覆盖。
  - 若希望强制只连接已有 Chrome，可使用 `--require-browser`（未检测到将直接报错）。
  - 若不想看到提示文案，可加 `--quiet`。
  - `--timeout` 若小于 1000，将自动按“秒”换算为毫秒并提示。

可选说明：
- 如果你不想复用实例，可加 `--isolated` 启动独立浏览器。

## 连接已开启的 Chrome（远程调试）

如果你希望脚本优先连接“已打开的 Chrome”，需先开启远程调试端口：

```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=~/.chrome_mcp/chrome-profile"
```

也可以指定不同端口：

```bash
python3 scripts/chrome_mcp.py --browser-url http://127.0.0.1:9333 navigate --url https://example.com
```

## 工作流

1. 打开或选择页面：`new-page` 或 `list-pages` + `select-page`。
2. 导航并等待页面就绪：`navigate` + `wait`。
3. 获取可操作元素：`snapshot` → 解析 `uid`。
4. 执行动作：`click`、`fill`、`press`。
5. 调试与诊断：`list-console`、`list-network`、`trace-start`/`trace-stop`。
6. 输出结果：`screenshot` 或 `call evaluate_script` 抽取结构化信息。

## 常用命令示例

```bash
# 查看是否会复用已开的 Chrome（不会启动新实例）
python3 scripts/chrome_mcp.py status

# 打开页面
python3 scripts/chrome_mcp.py new-page --url https://example.com

# 截全页
python3 scripts/chrome_mcp.py screenshot --full-page

# 页面快照（a11y 树）
python3 scripts/chrome_mcp.py snapshot

# 点击与输入
python3 scripts/chrome_mcp.py click --uid <UID>
python3 scripts/chrome_mcp.py fill --uid <UID> --value "hello"
python3 scripts/chrome_mcp.py press --key Enter

# 等待页面加载完成（无需传 --text）
python3 scripts/chrome_mcp.py wait

# 等待指定文本出现
python3 scripts/chrome_mcp.py wait --text "README"
```

trace 说明：
- `trace-stop` 若出错，会将结果写入 `*_error.json` 并返回非 0 退出码。

## 快照解析（提取 uid）

```bash
# MCP: take_snapshot 生成的文件
python3 scripts/snapshot_extract.py --input /tmp/page.snapshot
```

## 参考

- 工具与参数速查：`references/tool-reference.md`
- 入口脚本：`scripts/chrome_mcp.py`
