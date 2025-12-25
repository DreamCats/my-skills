---
name: lark-send-msg
description: 使用 lark-cli send-message 向飞书用户或群聊发送消息，构造 content JSON 并自动判断 msg_type（text/post/image/file/audio/media/sticker/interactive/share_chat/share_user/system）。当用户需要“发送飞书消息”“把内容转成消息 JSON”“选择消息类型”“用 lark-cli 发送消息/回复消息/编辑消息”时使用。
---

# lark-send-msg

## 目标

- 通过 lark-cli send-message 发送消息
- 根据用户内容选择 msg_type，并构造 content JSON 字符串
- 优先覆盖 text 与 post，必要时覆盖媒体/卡片/系统消息

## 输入收集

- 询问或确认：
  - 接收者 ID 与类型：open_id / union_id / user_id / email / chat_id
  - 消息意图：普通文本、富文本、图片/文件/音视频、卡片、群名片/个人名片、系统分割线
  - 是否需要 @ 用户、链接、列表、代码块、图片等格式
  - 是否需要幂等：`--uuid`（可选）

## 消息类型判定（无明确指定时）

- 优先使用 `text`：单段短文本、少量换行、无复杂排版
- 使用 `post`：需要 Markdown 格式（列表、代码块、引用、分割线）、多段落、@、链接、图片/视频混排
  - 推荐以 `md` 标签承载 Markdown 内容（参考 `references/message_content.md`）
- 使用 `image` / `file` / `audio` / `media` / `sticker`：用户提供已上传的 `image_key` 或 `file_key`
- 使用 `interactive`：用户提供卡片 JSON / template_id / card_id
- 使用 `share_chat` / `share_user`：用户要求分享群名片/个人名片
- 使用 `system`：需要系统分割线（仅 tenant_access_token，且 p2p 生效）

## content JSON 构建

- `content` 必须是 JSON 字符串（需要转义）
- 推荐用临时 JSON 文件或脚本生成转义字符串
- 详细字段结构见 `references/message_content.md`

示例：

text

```bash
lark-cli send-message <RECEIVE_ID> \
  --receive-id-type open_id \
  --msg-type text \
  '{"text":"你好，消息已发送"}'
```

post + Markdown

```bash
lark-cli send-message <RECEIVE_ID> \
  --receive-id-type open_id \
  --msg-type post \
  '{"zh_cn":{"title":"通知","content":[[{"tag":"md","text":"**更新**\\n- item1\\n- item2"}]]}}'
```

## 发送与校验

- 使用 `lark-cli send-message` 输出响应
- 如失败，检查：
  - `receive_id` 与 `--receive-id-type` 匹配
  - `msg_type` 与 `content` 结构一致
  - JSON 是否转义与压缩为单行
  - 权限与应用可用范围

## 注意事项

⚠️ **重要**：`lark-cli send-message` 命令的参数格式如下：
- 接收者ID（邮箱/用户ID等）必须作为**位置参数**直接放在命令后面
- 使用 `--receive-id-type` 指定接收者ID类型（email/open_id/union_id/user_id/chat_id）
- 消息内容JSON必须作为**最后一个参数**

✅ 正确示例：
```bash
lark-cli send-message --receive-id-type email --msg-type text maifeng@bytedance.com '{"text":"笑话内容"}'
```

❌ 错误示例（不要这样用）：
```bash
lark-cli send-message --email maifeng@bytedance.com --msg-type text --content '{"text":"笑话内容"}'
```

## 参考

- 需要消息内容结构体时读取：`references/message_content.md`
