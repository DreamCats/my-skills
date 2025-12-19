---
name: byted-lark-cli
description: Lark CLI工具集 - 提供查询飞书文档、知识空间管理、消息发送、文件操作等功能。使用场景包括：文档内容查询、知识库节点信息获取、文档块操作、媒体文件上传、消息发送、群聊搜索等。支持lark-cli命令、飞书文档查询、bytedance.larkoffice.com相关操作。
---

# Lark CLI 工具技能

## Purpose

提供使用 Lark CLI 工具的完整指导，包括安装配置、常用命令、实际应用场景和最佳实践。

## When to Use This Skill

当用户需要：

- 查询飞书文档内容或知识空间信息
- 进行文档的创建、编辑和块操作
- 发送各类消息（文本、富文本、图片、文件等）
- 上传媒体文件到文档或表格
- 搜索群聊或获取历史消息
- 批量处理文档操作
- 配置和调试 Lark CLI 工具

## Quick Start

**验证安装**

```bash
# 检查 lark-cli 是否可用
which lark-cli
lark-cli --help
```

### 核心命令速查

```bash
# 获取知识空间节点
lark-cli get-node <node_token>

# 查询文档内容
lark-cli get-content <document_id>

# 创建新文档
lark-cli create-document --title "文档标题"

# 发送消息
lark-cli send-message <receive_id> --receive-id-type <type> --msg-type <type> '<content_json>'

# 上传文件
lark-cli upload-media <file_path> <parent_type> <parent_node>

# 添加内容到文档（支持从文件、目录或直接内容添加）
lark-cli add-content <DOCUMENT_ID> <SOURCE> [选项]
```

## Document Operations

### 查询文档信息

**获取文档元数据：**

```bash
# 获取知识空间节点信息
lark-cli get-node wiki_node_token

# 输出格式控制
lark-cli --format json get-node node_token
```

**读取文档内容：**

```bash
# 获取文档纯文本
lark-cli get-content docx_token

# 详细模式显示
lark-cli -v get-content docx_token
```

### 文档创建与编辑

**创建文档：**

```bash
# 创建空文档
lark-cli create-document

# 在指定位置创建
lark-cli create-document --folder-token folder_token --title "新文档"
```

**内容添加与块操作：**

```bash
# 添加 Markdown 内容到文档
lark-cli add-content doc_id "# 标题\n\n内容" --source-type content

# 添加本地文件内容
lark-cli add-content doc_id ./source.md

# 批量添加目录中的所有 Markdown 文件
lark-cli add-content doc_id ./docs --source-type dir --pattern "*.md"

# 获取所有块
lark-cli get-blocks doc_id --all

```

## Message Operations

### 发送消息

发消息前，如果是复杂消息，切记参考，[消息格式](reference/message.md)

**文本消息：**

```bash
lark-cli send-message user_open_id_123 \
  --receive-id-type open_id \
  --msg-type text \
  '{
    "text":"你好，这是一条测试消息"
  }'
```

**富文本消息：**

```bash
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

**图片/文件消息：**

```bash
# 先上传获取 key
lark-cli upload-media ./image.png docx_image block_id

# 发送图片消息
lark-cli send-message user_id \
  --receive-id-type open_id \
  --msg-type image \
  '{"image_key":"img_xxx"}'
```

### 搜索与历史

**搜索群聊：**

```bash
# 搜索所有群
lark-cli search-chats

# 关键词搜索
lark-cli search-chats --query "关键词"

# 分页搜索
lark-cli search-chats --page-size 50 --page-token token
```

**获取历史消息：**

```bash
# 获取群聊历史
lark-cli get-message-history --container-id-type chat --container-id chat_id

# 时间范围筛选
lark-cli get-message-history \
  --container-id-type chat \
  --container-id chat_id \
  --start-time 1608594809 \
  --end-time 1609296809
```

## File Operations

### 文件读写

```bash
# 读取文件
lark-cli read-file /path/to/file.txt

# 写入文件（Base64编码）
CONTENT=$(echo "内容" | base64)
lark-cli write-file /path/to/file.txt "$CONTENT"
```

### 媒体上传

```bash
# 上传图片到文档
lark-cli upload-media image.png docx_image block_id

# 上传文件到文档
lark-cli upload-media document.pdf docx_file block_id --checksum checksum

# 上传到表格
lark-cli upload-media chart.png sheet_image sheet_token
```

## 权限管理

```bash
# 添加用户编辑权限
lark-cli add-permission doc_token \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm edit \
  --notification

# 添加部门查看权限
lark-cli add-permission sheet_token \
  --doc-type sheet \
  --member-type opendepartmentid \
  --member-id dept_id \
  --perm view
```

## Output Formats

Control output format for different use cases:

```bash
# 文本输出（默认）
lark-cli get-node token

# JSON 输出（便于脚本处理）
lark-cli --format json get-node token

# 详细日志
lark-cli -v get-content doc_id
```

## Common Use Cases

### 1. 文档信息查询工作流

```bash
# 查询知识空间结构
lark-cli get-node space_token --obj-type wiki

# 获取文档内容
lark-cli get-content docx_token --format json > content.json

# 提取所有文档块
lark-cli get-blocks doc_id --all > blocks.json
```

### 2. 消息通知自动化

```bash
# 批量发送通知
while read user_id; do
  lark-cli send-message $user_id \
    --receive-id-type open_id \
    --msg-type text \
    '{"text":"重要通知：请查看更新"}'
done < user_list.txt
```

## Troubleshooting

### 常见错误解决

1. **认证失败**

   - 检查 `.env` 文件是否在可执行文件同目录
   - 验证 `APP_ID` 和 `APP_SECRET` 是否正确

2. **权限不足**

   - 确保应用有相应 API 权限
   - 检查文档访问权限

3. **文件上传失败**
   - 验证文件路径和格式
   - 检查 parent_node 是否有效

### 调试技巧

```bash
# 启用详细日志
lark-cli -v <command>

# 使用 JSON 输出查看详细响应
lark-cli --format json <command>

# 测试 API 连接
lark-cli get-node test_token -v
```

## Best Practices

1. **批量操作时使用 JSON 格式**，便于脚本处理
2. **大文档查询时使用分页参数**，避免超时
3. **敏感信息使用环境变量**，不要硬编码在脚本中
4. **错误处理时检查退出码**，确保操作成功
5. **定期更新 access_token**，保持 API 访问有效

## Resources

- [API Endpoints Reference](references/api_endpoints.md)
- [Examples Collection](references/examples.md)
- [Troubleshooting Guide](references/troubleshooting.md)
