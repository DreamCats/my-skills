---
name: lark-md-to-doc
description: 将 Markdown 文本自动渲染为飞书云文档，按指令块调用 lark-cli 创建/写入内容，并支持高亮块、画板与 PlantUML/Mermaid 图表。适用于任何需要 Markdown → 飞书文档自动落地的场景。
---

# Lark Markdown to Doc

## 概览

以 Markdown 为输入，通过 lark-cli 分段写入飞书文档，并在遇到指令块时自动创建高亮块或画板并导入图表。

## 工作流（Markdown → 飞书文档）

1. 准备 Markdown 输入（文件路径）。
2. 选择写入目标：已有文档 `--doc-id` 或新建文档 `--title`。
3. 使用脚本解析指令块并调用 lark-cli 渲染。
4. 用 `get-content/get-blocks` 复核结构，必要时迭代。

## 脚本：Markdown 分段渲染

使用 `scripts/render_lark_doc.py` 读取 Markdown，按段调用 lark-cli：

```bash
# 先进入技能目录（重要），或者使用绝对路径
cd /Users/bytedance/.codex/skills/lark-md-to-doc

# 创建新文档并渲染
python3 scripts/render_lark_doc.py --md ./doc.md --title "文档标题" [--folder-token <token>]

# 渲染到已有文档
python3 scripts/render_lark_doc.py --md ./doc.md --doc-id <DOC_ID>
```

指令块语法：

````markdown
```plantuml
@startuml
Alice -> Bob: Hello
@enduml
```

```mermaid
sequenceDiagram
  A->>B: Hi
```

```callout type=warning
这里是高亮块内容
```
````

说明：

- `plantuml` / `mermaid` 会自动创建画板并导入图表。
- `callout` 会创建高亮块；可选参数：`type=info|warning|error|success`。
- 非指令块的普通代码块会按原样写入 Markdown。

## 模板与参考

- 通用 Markdown 模板：`assets/markdown-template.md`
- PlantUML 安全子集：`references/plantuml-safe.md`
- 渲染脚本：`scripts/render_lark_doc.py`
