---
name: create-lark-doc
description: 使用 lark-cli 创建/写入飞书云文档的技能，输出高质感排版的 Markdown 文档，包含高亮块、画板与 PlantUML 图表。用户需要技术方案、项目方案、方案评审等“高大上”文档，并希望用 Markdown 模板与 lark-cli 自动落地时使用。
---

# Create Lark Doc

## 概览
用 Markdown 作为唯一事实来源，生成高质量技术方案文档，并通过 lark-cli 写入飞书云文档，按需加入高亮块、画板与 PlantUML 图。

## 工作流（技术方案）
1. 收集输入：标题、受众、范围、约束、关键决策、需要的图表类型与位置。
2. 产出 Markdown 草稿（使用模板与布局规则）。
3. 用 lark-cli 创建文档并写入 Markdown。
4. 添加高亮块与画板；在画板导入 PlantUML 图表。
5. 用 get-content/get-blocks 验证结构并迭代。

## 布局规则（高质感、布局舒服）
- 仅一个 H1 标题，可加一行副标题；紧跟一行紧凑元信息（负责人、日期、状态）。
- 段落短小（2~4 行），列表优先用要点。
- H2 作为主章节，H3 作为子章节，避免过深层级。
- 章节之间留空行，必要时用分割线降低密度。
- 顶部保留 TL;DR 与“决策/下一步”。
- 关键结论/风险/待确认问题用高亮块承载。

## 图片占位符
统一使用 Markdown 占位符，方便后续替换：
- `![Diagram: <short desc>](IMAGE_PLACEHOLDER_<SLUG>)`
- `![Screenshot: <short desc>](IMAGE_PLACEHOLDER_<SLUG>)`

## 图表选择
- 时序图：跨服务请求/响应链路。
- 活动/流程图：业务或操作流程。
- 状态图：生命周期或状态迁移。
- 类图/ER 图：数据模型与结构。
PlantUML 仅使用 `references/plantuml-safe.md` 的安全语法子集。

## Lark CLI 命令范式
创建文档：

```bash
lark-cli create-document --title "..." [--folder-token <token>]
```

写入 Markdown：

```bash
lark-cli add-content <DOC_ID> "<markdown>" --source-type content
lark-cli add-content <DOC_ID> ./doc.md
```

添加高亮块：

```bash
lark-cli add-callout <DOC_ID> "..." --callout-type warning --icon "!"
```

添加画板：

```bash
lark-cli add-board <DOC_ID> [--parent-id <block_id>] [--index <n>]
```

导入 PlantUML：

```bash
lark-cli import-diagram <WHITEBOARD_ID> "<puml>" --source-type content --syntax plantuml
```

校验：

```bash
lark-cli get-content <DOC_ID>
lark-cli get-blocks <DOC_ID> --all
```

## 模板与参考
- 技术方案模板：`assets/tech-proposal-template.md`
- PlantUML 安全子集：`references/plantuml-safe.md`
