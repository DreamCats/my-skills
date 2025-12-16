# get-content 命令使用说明

## 功能
获取文档的原始内容

## 基本用法
```bash
lark-cli get-content <DOCUMENT_ID> [选项]
```

## 参数
- `DOCUMENT_ID` (必需): 文档 ID

## 选项
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 示例

### 基本查询
```bash
# 获取文档内容（JSON 格式输出）
lark-cli get-content doc_xxx123456789

# 获取文档内容（文本格式输出）
lark-cli get-content doc_xxx123456789 --format text
```

### 调试模式
```bash
# 启用详细日志输出
lark-cli -v get-content doc_xxx123456789
```

## 返回内容结构
返回的文档内容包含以下信息：
- `content`: 文档的原始内容（Markdown 格式）
- 文档中的所有文本、格式和结构信息

## 常见用途
1. 备份文档内容
2. 文档内容分析
3. 文档迁移
4. 内容审核和检查

## 注意事项
- 只能获取有权限访问的文档
- 返回的是文档的原始 Markdown 内容
- 不包含文档的评论和协作信息