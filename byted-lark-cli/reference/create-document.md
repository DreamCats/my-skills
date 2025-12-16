# create-document 命令使用说明

## 功能
创建新的云文档

## 基本用法
```bash
lark-cli create-document [选项]
```

## 选项
- `--folder-token <TOKEN>`: 文件夹 token（可选）
- `--title <TITLE>`: 文档标题（可选，1-800字符）
- `-v, --verbose`: 详细输出模式
- `--format <FORMAT>`: 输出格式，支持 `text` 或 `json`（默认: json）

## 示例

### 创建空白文档
```bash
# 创建空白文档
lark-cli create-document

# 创建带标题的文档
lark-cli create-document --title "我的新文档"
```

### 在指定文件夹创建
```bash
# 在指定文件夹创建文档
lark-cli create-document --folder-token folder_xxx123

# 在指定文件夹创建带标题的文档
lark-cli create-document --folder-token folder_xxx123 --title "项目计划书"
```

### 调试模式
```bash
# 启用详细日志输出
lark-cli -v create-document --title "测试文档"
```

## 返回信息
创建成功后返回：
- `document_id`: 文档 ID
- `document_url`: 文档访问链接
- 其他文档元数据信息

## 常见用途
1. 快速创建新文档
2. 批量创建文档模板
3. 在特定文件夹中组织文档
4. 自动化文档创建流程

## 注意事项
- 如果不指定文件夹，文档将创建在默认位置
- 标题长度限制为 1-800 字符
- 需要有创建文档的权限