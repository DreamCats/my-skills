# 文件相关命令使用说明

## read-file 命令

### 功能
读取文件内容和大小

### 用法
```bash
lark-cli read-file <FILE_PATH>
```

### 参数
- `FILE_PATH` (必需): 文件路径

### 示例
```bash
# 读取本地文件
lark-cli read-file ./document.txt

# 读取绝对路径文件
lark-cli read-file /Users/username/Documents/file.pdf
```

### 返回信息
- 文件内容（Base64 编码）
- 文件大小（字节）

---

## write-file 命令

### 功能
写入文件内容

### 用法
```bash
lark-cli write-file <FILE_PATH> --content <CONTENT> [选项]
```

### 必需参数
- `FILE_PATH`: 文件路径
- `--content <CONTENT>`: 文件内容（Base64 编码）

### 选项
- `--overwrite`: 覆盖已存在的文件

### 示例
```bash
# 写入新文件
lark-cli write-file ./newfile.txt --content "SGVsbG8gV29ybGQ="

# 覆盖现有文件
lark-cli write-file ./existing.txt --content "SGVsbG8gV29ybGQ=" --overwrite
```

---

## upload-media 命令

### 功能
上传媒体文件

### 用法
```bash
lark-cli upload-media <FILE_PATH> --parent-type <TYPE> --parent-node <NODE> [选项]
```

### 必需参数
- `FILE_PATH`: 文件路径
- `--parent-type <TYPE>`: 上传点类型
  - 支持类型：`doc_image`、`docx_image`、`sheet_image`、`doc_file`、`docx_file`
- `--parent-node <NODE>`: 上传点 token（目标云文档 token 或 block_id）

### 选项
- `--checksum <CHECKSUM>`: Adler-32 校验和（可选）
- `--extra <EXTRA>`: 额外信息，格式: `{"drive_route_token":"文档token"}`（可选）

### 示例

#### 上传图片到文档
```bash
# 上传图片到文档
lark-cli upload-media ./image.png \
  --parent-type doc_image \
  --parent-node doc_xxx123

# 上传图片到文档块
lark-cli upload-media ./chart.png \
  --parent-type docx_image \
  --parent-node block_xxx456
```

#### 上传文件到表格
```bash
# 上传文件到表格
lark-cli upload-media ./report.pdf \
  --parent-type sheet_image \
  --parent-node sheet_xxx789
```

#### 带校验和上传
```bash
# 上传并验证文件完整性
lark-cli upload-media ./large-file.zip \
  --parent-type doc_file \
  --parent-node doc_xxx123 \
  --checksum 12345678
```

### 返回信息
- 文件上传状态
- 文件 ID 和访问链接
- 文件元数据信息

## 通用选项
所有文件命令都支持：
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 注意事项
1. **文件大小限制**：不同类型的上传点可能有不同的文件大小限制
2. **文件格式**：确保文件格式与上传点类型匹配
3. **网络稳定性**：大文件上传建议使用稳定网络
4. **权限要求**：需要有目标文档的编辑权限