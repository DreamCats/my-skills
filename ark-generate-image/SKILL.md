---
name: ark-generate-image
description: 使用 ark-cli generate 根据文本提示生成图片并获取返回 URL；当用户需要指定尺寸、解析输出或稳定拿到图片链接时使用。
---

# Ark 图片生成

## 适用场景
- 用户要求通过 ark-cli 生成图片
- 需要稳定解析图片 URL
- 需要指定图片尺寸（最低 2048x2048）

## 命令与入参
`ark-cli generate <PROMPT> [--size 2048x2048] [--format text|json] [--verbose]`

- PROMPT：必填，图片描述提示词
- --size：可选，格式 `宽x高`，最低 `2048x2048`，默认 `2048x2048`
- --format：可选，`text` 或 `json`，默认 `text`；需稳定解析 URL 时使用 `json`
- --verbose：可选，输出详细日志

## 出参与解析
- `--format json`：输出 JSON，包含图片 `url` 字段（用于直连图片）
- `--format text`：输出文本；若需要 URL，优先改用 `--format json`

## 标准流程
1. 让用户提供图片提示词与尺寸需求；未给尺寸则默认 `2048x2048`
2. 执行命令：`ark-cli generate "<PROMPT>" --size <SIZE> --format json`
3. 解析 JSON 中 `url` 并返回给用户

## 示例
命令：
`ark-cli generate "a cinematic city skyline at sunset" --size 2048x2048 --format json`

期望输出（示意）：
```
{"url":"https://..."}
```

## 交互要点
- 若输出中未找到 `url`，提示用户改用 `--format json` 并重试
- 不擅自改写用户提示词；必要时先确认
