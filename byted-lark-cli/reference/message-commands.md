# 消息相关命令使用说明

## send-message 命令

### 功能

发送消息

### 用法

```bash
lark-cli send-message <RECEIVE_ID> --receive-id-type <TYPE> --msg-type <MTYPE> --content <CONTENT> [选项]
```

### 必需参数

- `RECEIVE_ID`: 消息接收者 ID
- `--receive-id-type <TYPE>`: 接收者 ID 类型
  - 支持类型：`open_id`、`union_id`、`user_id`、`email`、`chat_id`
- `--msg-type <MTYPE>`: 消息类型
  - 支持类型：`text`、`post`、`image`、`file`、`audio`、`media`、`sticker`、`interactive`、`share_chat`、`share_user`、`system`
- `--content <CONTENT>`: 消息内容（JSON 格式字符串）

### 选项

- `--uuid <UUID>`: 唯一标识符，用于幂等控制（可选）

### 示例

#### 发送文本消息

```bash
# 发送简单文本消息
lark-cli send-message user_open_id_123 \
  --receive-id-type open_id \
  --msg-type text \
  '{
    "text":"你好，这是一条测试消息"
  }'

# 发送富文本消息
lark-cli send-message user_open_id_123 \
  --receive-id-type open_id \
  --msg-type post \
  '{
    "zh_cn": {
      "title": "项目通知",
      "content": [
        [{"tag": "text", "text": "项目已更新："}],
        [{"tag": "a", "text": "查看详情", "href": "https://example.com"}]
      ]
    }
  }'
```

#### 发送文件消息

```bash
# 发送文件
lark-cli send-message user_open_id_123 \
  --receive-id-type open_id \
  --msg-type file \
  '{
    "file_key": "file_xxx123"
  }'
```

---

## search-chats 命令

### 功能

搜索群列表

### 用法

```bash
lark-cli search-chats [选项]
```

### 选项

- `--user-id-type <TYPE>`: 用户 ID 类型（默认: open_id）
- `--query <QUERY>`: 关键词搜索
- `--page-token <TOKEN>`: 分页标记
- `--page-size <SIZE>`: 分页大小（1-100，默认: 50）

### 示例

```bash
# 搜索所有群聊
lark-cli search-chats

# 按关键词搜索
lark-cli search-chats --query "项目讨论"

# 指定分页大小
lark-cli search-chats --page-size 20
```

---

## get-message-history 命令

### 功能

获取会话历史消息

### 用法

```bash
lark-cli get-message-history --container-id-type <CTYPE> --container-id <ID> [选项]
```

### 必需参数

- `--container-id-type <CTYPE>`: 容器类型
  - 支持类型：`chat`、`thread`
- `--container-id <ID>`: 容器 ID

### 选项

- `--start-time <TIME>`: 起始时间（秒级时间戳）
- `--end-time <TIME>`: 结束时间（秒级时间戳）
- `--sort-type <TYPE>`: 排序方式（默认: ByCreateTimeDesc）
  - 支持：`ByCreateTimeAsc`、`ByCreateTimeDesc`
- `--page-size <SIZE>`: 分页大小（1-50，默认: 20）
- `--page-token <TOKEN>`: 分页标记

### 示例

#### 获取群聊历史

```bash
# 获取最近消息
lark-cli get-message-history \
  --container-id-type chat \
  --container-id chat_xxx123

# 获取指定时间范围的消息
lark-cli get-message-history \
  --container-id-type chat \
  --container-id chat_xxx123 \
  --start-time 1640995200 \
  --end-time 1672531199

# 按时间升序获取
lark-cli get-message-history \
  --container-id-type chat \
  --container-id chat_xxx123 \
  --sort-type ByCreateTimeAsc
```

#### 获取话题历史

```bash
# 获取话题消息
lark-cli get-message-history \
  --container-id-type thread \
  --container-id thread_xxx456
```

## 通用选项

所有消息命令都支持：

- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 注意事项

1. **消息内容格式**：不同类型的消息需要不同的 JSON 格式
2. **权限要求**：需要有发送消息或查看消息的权限
3. **时间格式**：时间戳使用秒级 Unix 时间戳
4. **分页处理**：大量消息需要分页获取
