---
name: byted-logid
description: 字节日志ID工具集 - 提供生成字节日志ID的功能
---

## 命令位置

字节日志 ID 工具集 (byted-logid)， 存放在 scripts 目录下, 可以直接在终端中使用。

## 📋 详细使用说明

### 命令语法

```bash
logid [OPTIONS] <LOGID>
```

### 必需参数

| 参数    | 说明            | 示例                      |
| ------- | --------------- | ------------------------- |
| `LOGID` | 要查询的日志 ID | `"20240101-abc123def456"` |

### 可选参数

| 参数       | 短参数 | 说明                | 可选值             | 默认值 |
| ---------- | ------ | ------------------- | ------------------ | ------ |
| `--region` | `-r`   | 查询区域            | `cn`, `i18n`, `us` | 必需   |
| `--psm`    | `-p`   | 过滤的 PSM 服务名称 | 有效的 PSM 字符串  | 无过滤 |
| `--output` | `-o`   | 输出格式            | `text`, `json`     | `text` |

## 使用示例

### 基本命令

```bash
# 查询美区日志
.claude/skills/byted-logid/scripts/logid "20240101-abc123def456" --region us

# 多 PSM 过滤
.claude/skills/byted-logid/scripts/logid "20240101-abc123def456" --region i18n --psm "user.service" --psm "auth.service"

# JSON 输出
.claude/skills/byted-logid/scripts/logid "20240101-abc123def456" --region us --output json
```
