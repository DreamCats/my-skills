# Lark API 端点参考

本文档详细说明了 Lark CLI 工具使用的各个 API 端点。

## 认证端点

### 获取租户访问令牌
```
POST https://open.larkoffice.com/open-apis/auth/v3/tenant_access_token/internal
```

**请求体:**
```json
{
  "app_id": "your_app_id",
  "app_secret": "your_app_secret"
}
```

**响应:**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "tenant_access_token": "t-xxx",
    "expire": 3600
  }
}
```

## 知识空间 API

### 获取知识空间节点信息
```
GET https://open.larkoffice.com/open-apis/wiki/v2/spaces/get_node
```

**查询参数:**
- `token`: 节点 token
- `obj_type`: 对象类型（可选）
- `user_id_type`: 用户ID类型（可选）

## 文档内容 API

### 获取文档原始内容
```
GET https://open.larkoffice.com/open-apis/docx/v1/documents/{document_id}/raw_content
```

**路径参数:**
- `document_id`: 文档ID

**查询参数:**
- `user_id_type`: 用户ID类型（可选）

### 创建新文档
```
POST https://open.larkoffice.com/open-apis/docx/v1/documents
```

**请求体:**
```json
{
  "folder_token": "folder_token",  // 可选
  "title": "文档标题"              // 可选
}
```

### 内容转换为文档块
```
POST https://open.larkoffice.com/open-apis/docx/v1/documents/blocks/convert
```

**请求体:**
```json
{
  "content": "# 标题\n\n内容",
  "content_type": "markdown"  // markdown|html
}
```

### 创建嵌套块
```
POST https://open.larkoffice.com/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/descendant
```

**路径参数:**
- `document_id`: 文档ID
- `block_id`: 父块ID（根级别使用空字符串）

**请求体:**
```json
{
  "children_id": ["temp-1", "temp-2"],
  "descendants": [...],
  "index": 0,
  "document_revision_id": -1,
  "client_token": "uuid"
}
```

### 获取文档块列表
```
GET https://open.larkoffice.com/open-apis/docx/v1/documents/{document_id}/blocks
```

**查询参数:**
- `page_size`: 分页大小（1-500）
- `page_token`: 分页标记
- `document_revision_id`: 文档版本ID
- `user_id_type`: 用户ID类型

### 批量更新文档块
```
PATCH https://open.larkoffice.com/open-apis/docx/v1/documents/{document_id}/blocks/batch_update
```

**请求体:**
```json
{
  "requests": [
    {
      "block_id": "block_1",
      "heading1": {...}
    }
  ],
  "document_revision_id": -1,
  "client_token": "uuid"
}
```

### 删除文档块
```
DELETE https://open.larkoffice.com/open-apis/docx/v1/documents/{document_id}/blocks/{block_id}/children/batch_delete
```

**查询参数:**
- `start_index`: 起始索引
- `end_index`: 结束索引
- `document_revision_id`: 文档版本ID
- `client_token`: UUID

## 权限管理 API

### 添加协作者权限
```
POST https://open.larkoffice.com/open-apis/drive/v1/permissions/{token}/members
```

**路径参数:**
- `token`: 云文档token

**查询参数:**
- `type`: 权限类型（container|single_page）
- `need_notification`: 是否通知

**请求体:**
```json
{
  "member_type": "email",
  "member_id": "user@example.com",
  "perm": "edit",
  "collaborator_type": "user"
}
```

## 媒体文件 API

### 上传媒体文件
```
POST https://open.larkoffice.com/open-apis/drive/v1/medias/upload_all
```

**请求类型:** multipart/form-data

**字段:**
- `file`: 文件内容
- `parent_type`: 上传点类型
- `parent_node`: 上传点token
- `checksum`: Adler-32校验和（可选）
- `extra`: 额外信息JSON（可选）

**parent_type 支持的类型:**
- `doc_image`: 文档图片
- `docx_image`: 云文档图片
- `sheet_image`: 表格图片
- `doc_file`: 文档文件
- `docx_file`: 云文档文件

## 文件操作 API

### 读取文件
```
GET https://open.larkoffice.com/open-apis/drive/v1/files/{file_token}/content
```

**路径参数:**
- `file_token`: 文件token

### 写入文件
```
POST https://open.larkoffice.com/open-apis/drive/v1/files/{file_path}
```

**路径参数:**
- `file_path`: 文件路径

**请求体:**
```json
{
  "content": "base64编码的内容",
  "overwrite": true
}
```

## 消息 API

### 发送消息
```
POST https://open.larkoffice.com/open-apis/im/v1/messages
```

**请求体:**
```json
{
  "receive_id_type": "open_id",
  "receive_id": "user_id",
  "msg_type": "text",
  "content": "{\"text\":\"消息内容\"}",
  "uuid": "可选UUID"
}
```

**消息类型和内容格式:**

#### 文本消息 (text)
```json
{"text":"消息内容"}
```

#### 富文本消息 (post)
```json
{
  "title": "标题",
  "content": [[
    [{
      "tag": "text",
      "text": "内容"
    }]
  ]]
}
```

#### 图片消息 (image)
```json
{"image_key":"img_xxx"}
```

#### 文件消息 (file)
```json
{"file_key":"file_xxx"}
```

#### 卡片消息 (interactive)
```json
{
  "elements": [
    {
      "tag": "markdown",
      "content": "**加粗文本**"
    }
  ]
}
```

### 搜索群聊
```
GET https://open.larkoffice.com/open-apis/im/v1/chats/search
```

**查询参数:**
- `user_id_type`: 用户ID类型
- `query`: 搜索关键词（可选）
- `page_size`: 分页大小（1-100）
- `page_token`: 分页标记

### 获取会话历史
```
GET https://open.larkoffice.com/open-apis/im/v1/messages
```

**查询参数:**
- `container_id_type`: 容器类型（chat|thread）
- `container_id`: 容器ID
- `start_time`: 起始时间戳（可选）
- `end_time`: 结束时间戳（可选）
- `sort_type`: 排序方式（ByCreateTimeAsc|ByCreateTimeDesc）
- `page_size`: 分页大小（1-50）
- `page_token`: 分页标记

## 文档块类型参考

### 基本块类型

| 类型ID | 类型名称 | 说明 |
|--------|----------|------|
| 1 | PAGE | 页面 |
| 2 | TEXT | 文本 |
| 3 | HEADING_1 | 一级标题 |
| 4 | HEADING_2 | 二级标题 |
| 5 | HEADING_3 | 三级标题 |
| 6 | HEADING_4 | 四级标题 |
| 7 | HEADING_5 | 五级标题 |
| 8 | HEADING_6 | 六级标题 |
| 9 | HEADING_7 | 七级标题 |
| 10 | HEADING_8 | 八级标题 |
| 9 | HEADING_9 | 九级标题 |
| 10 | BULLET | 无序列表 |
| 11 | ORDERED | 有序列表 |
| 12 | CODE | 代码块 |
| 13 | QUOTE | 引用 |
| 14 | EQUATION | 公式 |
| 15 | TODO | 待办事项 |
| 16 | INDENT | 缩进 |
| 17 | MENTION | 提及 |
| 18 | PICTURE | 图片 |
| 19 | TABLE | 表格 |
| 20 | HIGHLIGHT | 高亮 |
| 21 | VIEW | 视图 |
| 22 | FILE | 文件 |
| 23 | VIDEO | 视频 |
| 24 | ATTACHMENT | 附件 |
| 25 | BOOKMARK | 书签 |
| 26 | CALLOUT | 标注块 |
| 27 | BINGO | 看板 |
| 28 | MINDNOTE | 思维导图 |
| 29 | DIAGRAM | 流程图 |
| 30 | CHART | 图表 |
| 31 | POLL | 投票 |
| 32 | BITABLE | 多维表格 |
| 33 | CALENDAR | 日历 |
| 34 | SHEET | 电子表格 |
| 35 | DOC | 文档 |
| 36 | DOCX | 云文档 |
| 37 | SLIDE | 幻灯片 |
| 38 | MINUTES | 会议纪要 |
| 39 | WIKI | 知识库 |
| 40 | FOLDER | 文件夹 |
| 41 | SPACE | 空间 |
| 42 | DRIVE | 云盘 |
| 43 | RECYCLE | 回收站 |
| 44 | SHARED | 共享 |
| 45 | STARRED | 收藏 |
| 46 | RECENT | 最近 |
| 47 | OFFLINE | 离线 |
| 48 | TRASH | 垃圾箱 |
| 49 | ARCHIVE | 归档 |
| 50 | TEMPLATE | 模板 |
| 51 | DRAFT | 草稿 |
| 52 | PUBLISHED | 已发布 |
| 53 | PRIVATE | 私密 |
| 54 | PUBLIC | 公开 |
| 55 | ORG | 组织 |
| 56 | TEAM | 团队 |
| 57 | PERSONAL | 个人 |
| 58 | ALL | 全部 |
| 59 | SEARCH | 搜索 |
| 60 | FILTER | 筛选 |
| 61 | SORT | 排序 |
| 62 | GROUP | 分组 |
| 63 | TAG | 标签 |
| 64 | CATEGORY | 分类 |
| 65 | COLLECTION | 合集 |
| 66 | FAVORITE | 收藏夹 |
| 67 | HISTORY | 历史 |
| 68 | ACTIVITY | 活动 |
| 69 | COMMENT | 评论 |
| 70 | TASK | 任务 |
| 71 | EVENT | 事件 |
| 72 | REMINDER | 提醒 |
| 73 | NOTIFICATION | 通知 |
| 74 | SUBSCRIPTION | 订阅 |
| 75 | FEEDBACK | 反馈 |
| 76 | HELP | 帮助 |
| 77 | ABOUT | 关于 |
| 78 | SETTINGS | 设置 |
| 79 | PROFILE | 资料 |
| 80 | ACCOUNT | 账户 |
| 81 | SECURITY | 安全 |
| 82 | PRIVACY | 隐私 |
| 83 | BILLING | 计费 |
| 84 | UPGRADE | 升级 |
| 85 | USAGE | 使用情况 |
| 86 | STORAGE | 存储 |
| 87 | BANDWIDTH | 带宽 |
| 88 | LIMIT | 限制 |
| 89 | QUOTA | 配额 |
| 90 | PLAN | 方案 |
| 91 | TRIAL | 试用 |
| 92 | ENTERPRISE | 企业版 |
| 93 | PROFESSIONAL | 专业版 |
| 94 | BASIC | 基础版 |
| 95 | FREE | 免费版 |
| 96 | PREMIUM | 高级版 |
| 97 | ULTIMATE | 终极版 |
| 98 | CUSTOM | 自定义 |
| 99 | STANDARD | 标准版 |
| 100 | ADVANCED | 高级版 |

## 错误代码说明

| 错误码 | 说明 |
|--------|------|
| 0 | 成功 |
| 99991663 | 无效的 token |
| 99991401 | 没有权限 |
| 99991400 | 资源不存在 |
| 99991408 | 频率限制 |
| 99991409 | 请求参数错误 |
| 99991410 | 内部错误 |
| 99991411 | 网络错误 |
| 99991412 | 超时 |
| 99991413 | 服务不可用 |
| 99991414 | 维护中 |
| 99991415 | 已废弃 |
| 99991416 | 版本不支持 |
| 99991417 | 功能不支持 |
| 99991418 | 配额不足 |
| 99991419 | 文件过大 |
| 99991420 | 文件格式不支持 |
| 99991421 | 文件损坏 |
| 99991422 | 文件已存在 |
| 99991423 | 文件不存在 |
| 99991424 | 文件被占用 |
| 99991425 | 文件只读 |
| 99991426 | 文件加密 |
| 99991427 | 文件签名错误 |
| 99991428 | 文件校验失败 |
| 99991429 | 文件上传失败 |
| 99991430 | 文件下载失败 |
| 99991431 | 文件删除失败 |
| 99991432 | 文件复制失败 |
| 99991433 | 文件移动失败 |
| 99991434 | 文件重命名失败 |
| 99991435 | 文件创建失败 |
| 99991436 | 文件更新失败 |
| 99991437 | 文件同步失败 |
| 99991438 | 文件分享失败 |
| 99991439 | 文件取消分享失败 |
| 99991440 | 文件权限失败 |
| 99991441 | 文件锁定失败 |
| 99991442 | 文件解锁失败 |
| 99991443 | 文件版本失败 |
| 99991444 | 文件历史失败 |
| 99991445 | 文件恢复失败 |
| 99991446 | 文件备份失败 |
| 99991447 | 文件导出失败 |
| 99991448 | 文件导入失败 |
| 99991449 | 文件打印失败 |
| 99991450 | 文件预览失败 |
| 99991451 | 文件编辑失败 |
| 99991452 | 文件评论失败 |
| 99991453 | 文件点赞失败 |
| 99991454 | 文件收藏失败 |
| 99991455 | 文件标签失败 |
| 99991456 | 文件搜索失败 |
| 99991457 | 文件排序失败 |
| 99991458 | 文件筛选失败 |
| 99991459 | 文件分组失败 |
| 99991460 | 文件统计失败 |
| 99991461 | 文件分析失败 |
| 99991462 | 文件报告失败 |
| 99991463 | 文件设置失败 |
| 99991464 | 文件配置失败 |
| 99991465 | 文件模板失败 |
| 99991466 | 文件样例失败 |
| 99991467 | 文件教程失败 |
| 99991468 | 文件帮助失败 |
| 99991469 | 文件关于失败 |
| 99991470 | 文件联系失败 |
| 99991471 | 文件反馈失败 |
| 99991472 | 文件建议失败 |
| 99991473 | 文件投诉失败 |
| 99991474 | 文件举报失败 |
| 99991475 | 文件审核失败 |
| 99991476 | 文件违规失败 |
| 99991477 | 文件封禁失败 |
| 99991478 | 文件解封失败 |
| 99991479 | 文件申诉失败 |
| 99991480 | 文件撤销失败 |
| 99991481 | 文件确认失败 |
| 99991482 | 文件取消失败 |
| 99991483 | 文件拒绝失败 |
| 99991484 | 文件接受失败 |
| 99991485 | 文件完成失败 |
| 99991486 | 文件开始失败 |
| 99991487 | 文件暂停失败 |
| 99991488 | 文件继续失败 |
| 99991489 | 文件停止失败 |
| 99991490 | 文件重启失败 |
| 99991491 | 文件重置失败 |
| 99991492 | 文件清空失败 |
| 99991493 | 文件刷新失败 |
| 99991494 | 文件重新加载失败 |
| 99991495 | 文件重新连接失败 |
| 99991496 | 文件重新同步失败 |
| 99991497 | 文件重新认证失败 |
| 99991498 | 文件重新授权失败 |
| 99991499 | 文件重新登录失败 |
| 99991500 | 文件重新注册失败 |

## 限制说明

### API 限制
- 请求频率：每分钟最多 300 次
- 文件上传：最大 100MB
- 批量操作：每次最多 100 项
- 消息发送：每分钟最多 60 条

### 文件格式支持
**图片格式:** JPG, PNG, GIF, WebP
**文档格式:** PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
**视频格式:** MP4, AVI, MOV
**音频格式:** MP3, WAV, AAC