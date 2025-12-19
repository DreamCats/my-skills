---
name: byted-logid
description: 字节日志 ID 工具 Skill，用于通过现有 logid CLI 脚本查询和解析字节日志 ID
---

# 字节 LogID 工具 Skill

## 概述

- 该 Skill 是一个 **调度与索引层（Orchestration Layer）**
- 该 Skill 本身 **不实现日志解析逻辑**，  
  而是负责：
  - 判断用户意图
  - 组织命令参数
  - 调用脚本
  - 解释执行结果

## 什么时候使用这个 Skill

当出现以下情况时，应使用该 Skill：

- 用户提供了一个字节日志 ID，希望查询或解析
- 用户询问如何使用 logid 查询日志
- 用户提到字节日志、logid、日志 ID、区域日志等

典型触发示例包括：

- “帮我查一下这个 logid”
- “解析这个字节日志 ID”
- “用 logid 查美区日志”

## 可用资源

### 脚本

- **scripts/logid**
  - 用途：查询和解析字节日志 ID
  - 使用方式：在终端中直接执行
  - 支持能力：
    - 按区域查询（`cn` / `i18n` / `us`）
    - 按 PSM 服务过滤
    - 支持文本或 JSON 输出

## 执行流程

当该 Skill 被触发时，Claude 应按照以下步骤执行：

1. **识别用户意图**

   - 判断用户是否需要：
     - 基础日志查询
     - 指定区域查询
     - 按 PSM 过滤
     - 结构化（JSON）输出

2. **构造命令**

   - 根据用户意图选择合适的参数：
     - `--region`
     - `--psm`
     - `--output`

3. **执行脚本**

   - 调用 `scripts/logid` 并传入构造好的参数

4. **解释结果**
   - 如有需要，向用户解释输出字段含义
   - 高亮关键日志信息

## 命令参考

### 命令格式

```bash
logid [OPTIONS] <LOGID>
```

必需参数

参数 说明
LOGID 需要查询的字节日志 ID

可选参数

参数 短参数 说明 可选值
--region -r 查询区域 cn, i18n, us
--psm -p 按 PSM 服务过滤 PSM 字符串
--output -o 输出格式 text, json

示例

示例 1：基础日志查询

用户：
帮我查一下这个 logid：20240101-abc123def456（美区）

Claude（使用该 Skill）：
• 构造带 --region us 的命令
• 执行脚本并返回解析结果

logid "20240101-abc123def456" --region us

示例 2：按多个 PSM 过滤

用户：
只看 user.service 和 auth.service 的日志

Claude（使用该 Skill）：
• 添加多个 --psm 参数
• 执行脚本并解释过滤后的结果

logid "20240101-abc123def456" --region i18n \
 --psm "user.service" \
 --psm "auth.service"

示例 3：JSON 格式输出

用户：
用 JSON 格式输出

Claude（使用该 Skill）：
• 添加 --output json
• 使用结构化结果便于后续分析

logid "20240101-abc123def456" --region us --output json

说明
• 该 Skill 以 logid 脚本作为唯一事实来源
• 命令行为变更应优先修改脚本，而非在此文件中重复说明
• SKILL.md 重点在于 “何时用 + 怎么调度”，而非脚本实现细节
