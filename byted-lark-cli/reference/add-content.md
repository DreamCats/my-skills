# add-content 命令使用说明

## 功能
添加内容到飞书文档（支持从文件、目录或直接内容添加）

## 基本用法
```bash
lark-cli add-content <DOCUMENT_ID> <SOURCE> [选项]
```

## 参数
- `DOCUMENT_ID` (必需): 目标文档 ID
- `SOURCE` (必需): 导入源（文件路径、目录路径或直接内容）

## 选项
- `--source-type <TYPE>`: 源类型
  - `file` (默认): 单个文件
  - `dir`: 目录
  - `content`: 直接内容
- `--content-type <CTYPE>`: 内容类型
  - `markdown` (默认): Markdown 格式
  - `html`: HTML 格式
- `--block-id <BLOCK_ID>`: 父块 ID（空字符串表示在根级别创建，默认: ""）
- `--index <INDEX>`: 插入位置索引（默认: -1 表示末尾）
- `--recursive`: 递归处理子目录（仅对目录模式有效）
- `--pattern <PATTERN>`: 文件匹配模式（如 "*.md"）
- `--batch-size <SIZE>`: 批处理的并发数（默认: 3）
- `--skip-existing`: 跳过已存在的文件
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 示例

### 导入单个文件
```bash
# 导入单个 Markdown 文件
lark-cli add-content doc_xxx123 ./document.md

# 导入 HTML 文件
lark-cli add-content doc_xxx123 ./document.html --content-type html

# 导入到指定位置
lark-cli add-content doc_xxx123 ./document.md --index 0
```

### 导入目录
```bash
# 导入整个目录
lark-cli add-content doc_xxx123 ./docs --source-type dir

# 递归导入目录（包含子目录）
lark-cli add-content doc_xxx123 ./docs --source-type dir --recursive

# 只导入特定类型的文件
lark-cli add-content doc_xxx123 ./docs --source-type dir --pattern "*.md"

# 设置并发数
lark-cli add-content doc_xxx123 ./docs --source-type dir --batch-size 5
```

### 导入直接内容
```bash
# 导入直接内容
lark-cli add-content doc_xxx123 "# 标题\n\n这是内容" --source-type content

# 从管道导入内容
echo "# 标题\n\n内容" | lark-cli add-content doc_xxx123 - --source-type content
```

### 高级用法
```bash
# 递归导入所有 Markdown 文件，跳过已存在的
lark-cli add-content doc_xxx123 ./docs \
  --source-type dir \
  --recursive \
  --pattern "*.md" \
  --skip-existing \
  --batch-size 10 \
  -v
```

## 导入统计
导入完成后会显示统计信息：
```
=== 导入统计 ===
  总数:     10
  成功:     8 (80.0%)
  导入失败: 1 (10.0%)
  读取失败: 1 (10.0%)
```

## 常见用途
1. 批量迁移文档到飞书
2. 知识库内容导入
3. 项目文档整理
4. 自动化文档更新

## 注意事项
- 确保有目标文档的编辑权限
- 大文件建议分批处理
- 网络不稳定时可调低并发数
- 导入失败会显示具体错误信息