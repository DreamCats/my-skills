---
name: lark-creatae-plantuml
description: 生成和校验飞书画板可用的 PlantUML（安全子集）。当用户需要根据自然语言生成 PlantUML，或提供 PlantUML 并要求在飞书画板可用/降级修复/去除不兼容语法时使用。
---

# Lark Creatae PlantUML

## 概览

生成或修复适配飞书画板的 PlantUML，严格使用安全子集。输出时仅给出一个 PlantUML 代码块；若发生降级或移除，需在代码块外用简短条目说明。

## 快速流程

1) 用户给出自然语言描述  
推断图类型 → 按安全子集生成 PlantUML → 输出代码块。  

2) 用户给出 PlantUML  
运行 `scripts/sanitize_plantuml.py` 进行规则检查与降级 → 输出修正版代码块 + 变更说明。

## 图类型判断（用户未说明时）

- **流程/步骤/审批/规则** → 活动图/流程图
- **调用链/接口交互/消息顺序** → 时序图
- **角色-功能** → 用例图
- **结构/类/关系** → 类图
- **组件/模块/技术路线图** → 组件图（容器+组件盒子）
- **架构图/企业架构/分层架构** → 优先 ArchiMate 原生语法（若飞书渲染失败，退回组件图）
- **实体/字段/表关系** → ER 图
- **思维导图/层级梳理** → 思维导图（不稳定时改用活动图模拟）
- **状态图** → 优先转为活动图表达状态流转，并在说明中标记转换原因

## 安全子集参考

使用并遵守 `references/plantuml-safe-subset.md` 的语法清单。若存在冲突，以“安全子集”为准。

## 输出规范

- 只输出一个 PlantUML 代码块（默认 `@startuml`...`@enduml`，思维导图用 `@startmindmap`...`@endmindmap`）。
- 若有降级/移除，代码块外以简短条目说明修改点。
- 不输出多余的伪代码或额外图示。
- 类图成员块可用，但请避免可见性标记（`+` `-` `#` `~`）。
- 输出时不要包含行首缩进（飞书画板粘贴解析更稳定）。
- 避免方向控制指令（如 `left to right direction`）。
- ArchiMate 采用原生语法（`!include` / `skinparam` / `sprite` / `legend` 可保留），仍需无缩进；若渲染失败则改用组件图。

## 脚本

使用 `scripts/sanitize_plantuml.py` 对用户给定的 PlantUML 进行自动降级：

```bash
python3 scripts/sanitize_plantuml.py input.puml --output fixed.puml --report report.txt
python3 scripts/sanitize_plantuml.py input.puml --output fixed.puml --report report.txt --allow-archimate
python3 scripts/sanitize_plantuml.py input.puml --output fixed.puml --report report.txt --archimate-raw
```

行为：
- 移除 `!define` 等预处理/宏指令
- 移除 `skinparam` 等样式指令
- 清理常见颜色标记
- 缺失 `@startuml/@enduml` 时自动补齐  

读取 `report.txt` 生成变更说明。若包含 ArchiMate 语法，脚本会自动进入原生态模式；也可显式使用 `--archimate-raw`。
