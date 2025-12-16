# Lark CLI 使用示例集合

本文档提供了 Lark CLI 工具的常用示例和使用场景。

## 文档查询示例

### 基础查询
```bash
# 查询文档内容
lark-cli get-content docx_xxx

# JSON 格式输出
lark-cli --format json get-content docx_xxx

# 查询知识空间节点
lark-cli get-node wiki_xxx

# 查询节点并指定对象类型
lark-cli get-node node_xxx --obj-type docx
```

### 高级查询
```bash
# 获取文档块信息
lark-cli get-blocks docx_xxx

# 获取所有块（自动分页）
lark-cli get-blocks docx_xxx --all

# 分页获取
lark-cli get-blocks docx_xxx --page-size 100

# 使用分页标记
lark-cli get-blocks docx_xxx --page-token "next_page_token"
```

## 文档创建示例

### 创建空文档
```bash
# 创建无标题文档
lark-cli create-document

# 创建带标题文档
lark-cli create-document --title "项目文档"

# 在指定文件夹创建
lark-cli create-document \
  --folder-token "folder_xxx" \
  --title "子文档"
```

### 创建文档并添加内容
```bash
# 1. 创建文档
DOC_INFO=$(lark-cli --format json create-document --title "新文档")
DOC_ID=$(echo $DOC_INFO | jq -r '.document_id')

# 2. 准备内容
CONTENT="# 标题\n\n这是文档内容。\n\n## 子标题\n\n子内容。"

# 3. 转换为块
BLOCKS=$(lark-cli --format json convert-blocks "$CONTENT")

# 4. 创建嵌套块
lark-cli create-nested-blocks "$DOC_ID" \
  "$(echo $BLOCKS | jq -r '.first_level_block_ids | join(",")')" \
  "$(echo $BLOCKS | jq -c '.blocks')"
```

## 内容操作示例

### Markdown 转换
```bash
# 简单 Markdown
lark-cli convert-blocks "# 标题\n\n段落内容"

# 从文件读取
lark-cli convert-blocks "$(cat document.md)"

# HTML 转换
lark-cli convert-blocks "<h1>标题</h1><p>内容</p>" --content-type html

# JSON 输出转换结果
lark-cli --format json convert-blocks "# 标题\n\n内容"
```

### 块操作
```bash
# 创建嵌套块
lark-cli create-nested-blocks doc_xxx \
  '["temp-1", "temp-2"]' \
  '[{
    "block_id": "temp-1",
    "block_type": 3,
    "heading1": {
      "elements": [{
        "text_run": {"content": "标题"}
      }]
    }
  }]'

# 在指定位置插入
lark-cli create-nested-blocks doc_xxx \
  --block-id parent_block \
  --index 2 \
  '["temp-1"]' \
  '[{"block_id":"temp-1","block_type":2,"text":{"elements":[{"text_run":{"content":"内容"}}]}}]'

# 批量更新块
lark-cli batch-update-blocks doc_xxx \
  --requests '[
    {
      "block_id": "block_1",
      "heading1": {
        "elements": [{
          "text_run": {
            "content": "新标题",
            "text_element_style": {"bold": true}
          }
        }]
      }
    }
  ]'

# 删除块
lark-cli delete-blocks doc_xxx parent_block 0 2
```

## 消息发送示例

### 文本消息
```bash
# 发送给用户
lark-cli send-message ou_xxx \
  --receive-id-type open_id \
  --msg-type text \
  '{"text":"你好，这是一条测试消息"}'

# 发送到群聊
lark-cli send-message oc_xxx \
  --receive-id-type chat_id \
  --msg-type text \
  '{"text":"群公告：项目已上线"}'
```

### 富文本消息
```bash
# 简单富文本
lark-cli send-message user_id \
  --receive-id-type open_id \
  --msg-type post \
  '{"title":"通知","content":[[{"tag":"text","text":"重要通知内容"}]]}'

# 复杂富文本
lark-cli send-message chat_id \
  --receive-id-type chat_id \
  --msg-type post \
  '{
    "title": "项目进度更新",
    "content": [
      [
        {
          "tag": "text",
          "text": "项目 ",
          "text_element_style": {"bold": true}
        },
        {
          "tag": "text",
          "text": "已完成 80%"
        }
      ]
    ]
  }'
```

### 图片消息
```bash
# 1. 先上传图片
UPLOAD_RESULT=$(lark-cli --format json upload-media ./image.png docx_image block_xxx)
IMAGE_KEY=$(echo $UPLOAD_RESULT | jq -r '.image_key')

# 2. 发送图片消息
lark-cli send-message user_id \
  --receive-id-type open_id \
  --msg-type image \
  "{\"image_key\":\"$IMAGE_KEY\"}"
```

### 卡片消息
```bash
# Markdown 卡片
lark-cli send-message user_id \
  --receive-id-type open_id \
  --msg-type interactive \
  '{
    "elements": [
      {
        "tag": "markdown",
        "content": "**重要提醒**：\n- 任务截止日期：明天\n- 请及时完成"
      }
    ]
  }'

# 交互卡片
lark-cli send-message chat_id \
  --receive-id-type chat_id \
  --msg-type interactive \
  '{
    "config": {
      "wide_screen_mode": true
    },
    "header": {
      "title": {
        "tag": "plain_text",
        "content": "任务审批"
      }
    },
    "elements": [
      {
        "tag": "div",
        "text": {
          "tag": "lark_md",
          "content": "申请：张三\n事项：请假一天"
        }
      },
      {
        "tag": "action",
        "actions": [
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "批准"
            },
            "type": "primary"
          },
          {
            "tag": "button",
            "text": {
              "tag": "plain_text",
              "content": "拒绝"
            },
            "type": "danger"
          }
        ]
      }
    ]
  }'
```

## 文件操作示例

### 读取文件
```bash
# 读取文件信息
lark-cli read-file /path/to/file.txt

# JSON 格式输出
lark-cli --format json read-file /path/to/file.txt

# 处理读取结果
RESULT=$(lark-cli --format json read-file document.txt)
SIZE=$(echo $RESULT | jq -r '.size')
CONTENT=$(echo $RESULT | jq -r '.content' | base64 -d)
```

### 写入文件
```bash
# 写入文本内容
echo "Hello World" | base64 > content.b64
lark-cli write-file /path/to/file.txt "$(cat content.b64)"

# 覆盖已存在文件
lark-cli write-file /path/to/file.txt "$(cat content.b64)" --overwrite

# 从文件复制
BASE64_CONTENT=$(base64 < source.txt)
lark-cli write-file /path/to/dest.txt "$BASE64_CONTENT"
```

### 媒体上传
```bash
# 上传图片到文档
lark-cli upload-media ./photo.jpg docx_image block_xxx

# 上传文件并添加校验和
CHECKSUM=$(python3 -c "import zlib; print(zlib.adler32(open('./document.pdf','rb').read()))")
lark-cli upload-media ./document.pdf docx_file block_xxx --checksum $CHECKSUM

# 上传到表格
lark-cli upload-media ./chart.png sheet_image sheet_xxx

# 批量上传
for file in ./images/*.png; do
  lark-cli upload-media "$file" docx_image block_xxx
  echo "已上传: $file"
done
```

## 群聊和消息历史示例

### 搜索群聊
```bash
# 搜索所有群
lark-cli search-chats

# 关键词搜索
lark-cli search-chats --query "项目"

# 大批量搜索
lark-cli search-chats --page-size 100

# 分页搜索
TOKEN=$(lark-cli --format json search-chats --page-size 20 | jq -r '.page_token')
lark-cli search-chats --page-token "$TOKEN"
```

### 获取历史消息
```bash
# 获取群聊历史
lark-cli get-message-history \
  --container-id-type chat \
  --container-id oc_xxx

# 时间范围查询
lark-cli get-message-history \
  --container-id-type chat \
  --container-id oc_xxx \
  --start-time 1608594809 \
  --end-time 1609296809

# 降序获取（最新在前）
lark-cli get-message-history \
  --container-id-type chat \
  --container-id oc_xxx \
  --sort-type ByCreateTimeDesc

# 获取指定数量
lark-cli get-message-history \
  --container-id-type chat \
  --container-id oc_xxx \
  --page-size 50
```

## 权限管理示例

### 添加用户权限
```bash
# 添加编辑权限
lark-cli add-permission doc_xxx \
  --doc-type docx \
  --member-type email \
  --member-id user@example.com \
  --perm edit \
  --notification

# 添加查看权限
lark-cli add-permission sheet_xxx \
  --doc-type sheet \
  --member-type openid \
  --member-id ou_xxx \
  --perm view
```

### 添加部门权限
```bash
# 部门查看权限
lark-cli add-permission doc_xxx \
  --doc-type docx \
  --member-type opendepartmentid \
  --member-id dept_xxx \
  --perm view

# 部门编辑权限
lark-cli add-permission sheet_xxx \
  --doc-type sheet \
  --member-type opendepartmentid \
  --member-id dept_xxx \
  --perm edit \
  --notification
```

## 实用脚本示例

### 批量文档导出
```bash
#!/bin/bash
# 导出文档列表中的所有文档

DOC_IDS_FILE="doc_ids.txt"
OUTPUT_DIR="./export"

mkdir -p "$OUTPUT_DIR"

while IFS= read -r doc_id; do
  echo "导出文档: $doc_id"

  # 获取内容
  lark-cli get-content "$doc_id" > "$OUTPUT_DIR/${doc_id}.txt"

  # 获取块信息
  lark-cli --format json get-blocks "$doc_id" --all > "$OUTPUT_DIR/${doc_id}_blocks.json"

  echo "完成: $doc_id"
  sleep 1
done < "$DOC_IDS_FILE"

echo "导出完成"
```

### 定时消息发送
```bash
#!/bin/bash
# 每日工作报告提醒

CHAT_ID="oc_xxx"
MESSAGE='{
  "title": "每日提醒",
  "content": [[
    {"tag": "text", "text": "请记得填写今日工作报告 📝"},
    {"tag": "text", "text": "\n截止时间：18:00"}
  ]]
}'

while true; do
  # 获取当前时间
  HOUR=$(date +%H)

  # 每天 17:00 发送提醒
  if [ "$HOUR" -eq 17 ]; then
    lark-cli send-message "$CHAT_ID" \
      --receive-id-type chat_id \
      --msg-type post \
      "$MESSAGE"

    # 等待到下一天
    sleep $((24 * 3600))
  else
    # 每小时检查一次
    sleep 3600
  fi
done
```

### 文档监控脚本
```bash
#!/bin/bash
# 监控文档更新

DOC_ID="docx_xxx"
LAST_REVISION=""

while true; do
  # 获取文档信息
  DOC_INFO=$(lark-cli --format json get-node "$DOC_ID")
  CURRENT_REVISION=$(echo $DOC_INFO | jq -r '.obj_edit_time')

  if [ "$CURRENT_REVISION" != "$LAST_REVISION" ] && [ -n "$LAST_REVISION" ]; then
    echo "文档已更新: $DOC_ID"

    # 发送通知
    lark-cli send-message "oc_xxx" \
      --receive-id-type chat_id \
      --msg-type text \
      '{"text":"文档监控：文档已被更新"}'
  fi

  LAST_REVISION="$CURRENT_REVISION"
  sleep 60  # 每分钟检查一次
done
```

## 组合使用示例

### 文档创建和分享流程
```bash
#!/bin/bash
# 完整的文档创建、内容填充和权限分享流程

# 1. 创建文档
echo "创建文档..."
DOC_RESULT=$(lark-cli --format json create-document --title "项目计划书")
DOC_ID=$(echo $DOC_RESULT | jq -r '.document_id')

# 2. 准备内容
echo "准备内容..."
CONTENT=$(cat << 'EOF'
# 项目计划书

## 项目背景
描述项目背景和目标

## 项目范围
- 功能模块 A
- 功能模块 B
- 功能模块 C

## 时间计划
1. 第一阶段：需求分析
2. 第二阶段：系统设计
3. 第三阶段：开发实施
4. 第四阶段：测试上线
EOF
)

# 3. 转换并创建块
echo "添加内容..."
BLOCKS=$(lark-cli --format json convert-blocks "$CONTENT")
lark-cli create-nested-blocks "$DOC_ID" \
  "$(echo $BLOCKS | jq -r '.first_level_block_ids | join(",")')" \
  "$(echo $BLOCKS | jq -c '.blocks')"

# 4. 添加协作者
echo "添加权限..."
lark-cli add-permission "$DOC_ID" \
  --doc-type docx \
  --member-type email \
  --member-id "team@example.com" \
  --perm edit \
  --notification

# 5. 发送通知
echo "发送通知..."
lark-cli send-message "oc_xxx" \
  --receive-id-type chat_id \
  --msg-type interactive \
  '{
    "elements": [
      {
        "tag": "markdown",
        "content": "**新文档已创建**\n\n项目计划书已完成初稿，请查阅：\nhttps://example.com/doc/'$DOC_ID'"
      }
    ]
  }'

echo "完成！文档ID: $DOC_ID"
```

### 数据导出和分析
```bash
#!/bin/bash
# 导出多个文档数据并进行分析

DOCS=(
  "docx_001"
  "docx_002"
  "docx_003"
)

OUTPUT_DIR="./analysis"
mkdir -p "$OUTPUT_DIR"

# 统计变量
TOTAL_DOCS=0
TOTAL_BLOCKS=0

for doc_id in "${DOCS[@]}"; do
  echo "处理文档: $doc_id"

  # 获取块信息
  BLOCKS_JSON="$OUTPUT_DIR/${doc_id}_blocks.json"
  lark-cli --format json get-blocks "$doc_id" --all > "$BLOCKS_JSON"

  # 统计块数量
  BLOCK_COUNT=$(jq '.items | length' "$BLOCKS_JSON")

  # 保存统计信息
  echo "$doc_id: $BLOCK_COUNT blocks" >> "$OUTPUT_DIR/stats.txt"

  ((TOTAL_DOCS++))
  ((TOTAL_BLOCKS += BLOCK_COUNT))

  sleep 1
done

# 生成分析报告
cat > "$OUTPUT_DIR/analysis_report.md" << EOF
# 文档分析报告

## 概览
- 文档总数：$TOTAL_DOCS
- 块总数：$TOTAL_BLOCKS
- 平均每文档块数：$((TOTAL_BLOCKS / TOTAL_DOCS))

## 详细统计
$(cat "$OUTPUT_DIR/stats.txt")
EOF

echo "分析完成，报告保存至：$OUTPUT_DIR/analysis_report.md"