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

- "帮我查一下这个 logid"
- "解析这个字节日志 ID"
- "用 logid 查美区日志"

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
     - `--region` / `-r`
     - `--psm` / `-p`
     - `--output` / `-o`

3. **执行脚本**

4. **解释结果**
   - 如有需要，向用户解释输出字段含义
   - 高亮关键日志信息

## 命令参考

### 命令格式

```bash
logid query [OPTIONS] --region <REGION> <LOGID>
```

### 必需参数

| 参数 | 说明 |
|------|------|
| `LOGID` | 要查询的日志 ID（通常是 UUID 格式） |
| `--region` / `-r` | 查询区域：`cn`、`i18n`、`us` |

### 可选参数

| 参数 | 短参数 | 说明 | 可选值 |
|------|--------|------|--------|
| `--psm` | `-p` | 过滤的 PSM 服务名称（可多次指定） | PSM 字符串 |
| `--output` | `-o` | 输出格式 | `text`（默认）、`json` |

### 区域说明

| 区域 | 说明 | URL |
|------|------|-----|
| `us` | 美区 | https://logservice-tx.tiktok-us.org |
| `i18n` | 国际化区域 | https://logservice-sg.tiktok-row.org |
| `cn` | 中国区 | 需要特殊配置 |

### 认证说明

需要在环境变量中配置对应区域的 `CAS_SESSION`：
- `CAS_SESSION_US`：美区认证凭据
- `CAS_SESSION_I18N`：国际化区域认证凭据
- `CAS_SESSION_CN`：中国区认证凭据

## 示例

### 示例 1：基础日志查询

用户：
```
帮我查一下这个 logid：550e8400-e29b-41d4-a716-446655440000（美区）
```

Claude（使用该 Skill）：
- 构造带 `--region us` 的命令
- 执行脚本并返回解析结果

```bash
logid query "550e8400-e29b-41d4-a716-446655440000" --region us
```

### 示例 2：按多个 PSM 过滤

用户：
```
只看 user.service 和 auth.service 的日志
```

Claude（使用该 Skill）：
- 添加多个 `--psm` 参数
- 执行脚本并解释过滤后的结果

```bash
logid query "550e8400-e29b-41d4-a716-446655440000" --region i18n \
  --psm "user.service" \
  --psm "auth.service"
```

### 示例 3：JSON 格式输出

用户：
```
用 JSON 格式输出
```

Claude（使用该 Skill）：
- 添加 `--output json`
- 使用结构化结果便于后续分析

```bash
logid query "550e8400-e29b-41d4-a716-446655440000" --region us --output json
```

## 其他命令

### 更新工具

```bash
logid update
```

将 logid 工具更新到最新版本。

### 查看帮助

```bash
logid --help          # 查看主帮助
logid query --help    # 查看 query 子命令帮助
```

## 说明

- 该 Skill 以 logid CLI 工具作为唯一事实来源
- 命令行为变更应优先修改工具本身，而非在此文件中重复说明
- SKILL.md 重点在于"何时用 + 怎么调度"，而非工具实现细节
